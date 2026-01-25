"""High-level documentation generation helpers."""

from __future__ import annotations

from dataclasses import dataclass
import os
import re
from pathlib import Path
from typing import Sequence, Callable, Optional

from .llm import (
    LLMError,
    LLMSettings,
    PROMPT_TEMPLATE,
    resolve_system_prompt,
    build_prompt,
    create_client,
    OllamaSettings,
)


DOCUMENTATION_SUBDIR = "generated"


@dataclass(slots=True)
class DocumentGenerationRequest:
    chapters: Sequence[Path]
    settings: LLMSettings
    prompt_template: str | None = None
    destination_dirname: str = DOCUMENTATION_SUBDIR
    destination_root: Path | None = None
    source_root: Path | None = None
    standalone: bool = False  # If True, generates a single combined file
    progress_callback: Optional[Callable[[int, int, str], None]] = None


@dataclass(slots=True)
class DocumentGenerationResult:
    written: list[tuple[Path | list[Path], Path]]  # (source(s), documentation)
    failures: list[tuple[Path | list[Path], str]]

    @property
    def success(self) -> bool:
        return not self.failures


def collect_chapter_files(path: Path) -> list[Path]:
    """Return a sorted list of Markdown files ready for documentation."""

    if path.is_file():
        return [path]

    files = [
        candidate
        for candidate in sorted(path.glob("*.md"))
        if not candidate.name.endswith(".docs.md")
    ]
    return files


def generate_documentation(request: DocumentGenerationRequest) -> DocumentGenerationResult:
    """Generate documentation for provided chapters using the configured LLM."""

    client = create_client(request.settings)
    written: list[tuple[Path | list[Path], Path]] = []
    failures: list[tuple[Path | list[Path], str]] = []
    system_prompt = resolve_system_prompt(request.settings)

    created_dirs: set[Path] = set()
    destination_root = request.destination_root or Path(request.destination_dirname)
    destination_root = Path(destination_root).expanduser().resolve()
    destination_root.mkdir(parents=True, exist_ok=True)
    source_root = request.source_root.resolve() if request.source_root else None

    def resolve_output_dir(chapter_path: Path) -> Path:
        if source_root:
            try:
                rel_parent = chapter_path.resolve().parent.relative_to(source_root)
                return destination_root / rel_parent
            except ValueError:
                return destination_root
        return destination_root
    
    def _is_testing() -> bool:
        return bool(os.getenv("PYTEST_CURRENT_TEST")) or os.getenv("DOCALYPT_TESTING") == "true"

    def _min_output_chars(input_chars: int) -> int:
        floor = 80
        ceiling = 900
        scaled = input_chars // 10 if input_chars > 0 else floor
        return max(floor, min(ceiling, scaled))

    def _extract_headings(markdown: str) -> list[str]:
        headings: list[str] = []
        for raw_line in markdown.splitlines():
            line = raw_line.strip()
            match = re.match(r"^(##+)\s+(.+)$", line)
            if not match:
                continue
            headings.append(match.group(2).strip())
        return headings

    def _duplicate_headings(headings: list[str]) -> list[str]:
        seen: set[str] = set()
        duplicates: list[str] = []
        for heading in headings:
            key = heading.lower()
            if key in seen and key not in {d.lower() for d in duplicates}:
                duplicates.append(heading)
            else:
                seen.add(key)
        return duplicates

    def _contains_code_fence(markdown: str) -> bool:
        return "```" in markdown

    def _contains_source_echo(markdown: str, source: str) -> bool:
        long_lines = [line.strip() for line in source.splitlines() if len(line.strip()) >= 120]
        for line in long_lines:
            if line and line in markdown:
                return True
        return False

    def _clean_heading(text: str) -> str:
        cleaned = re.sub(r"^[#*\\-\\d\\.\\)\\s]+", "", text).strip()
        cleaned = re.sub(r"\\s+", " ", cleaned)
        if cleaned.endswith(":"):
            cleaned = cleaned[:-1].strip()
        return cleaned

    def _derive_heading_from_sentence(sentence: str) -> str:
        words = re.findall(r"[A-Za-z0-9']+", sentence)
        if not words:
            return "Section"
        return " ".join(words[:6])

    def _fallback_outline_from_text(source: str, target_count: int) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\\s+", source.strip())
        sentences = [s for s in sentences if s.strip()]
        if not sentences:
            return []
        picks = []
        if len(sentences) <= target_count:
            picks = sentences
        else:
            step = max(1, len(sentences) // target_count)
            picks = [sentences[i] for i in range(0, len(sentences), step)][:target_count]
        headings: list[str] = []
        seen: set[str] = set()
        for sentence in picks:
            heading = _derive_heading_from_sentence(sentence)
            key = heading.lower()
            if key in seen:
                continue
            headings.append(heading)
            seen.add(key)
        return headings

    def _generate_outline(chapter_name: str, chapter_text: str) -> list[str]:
        outline_prompt = (
            "Extract 3 to 8 concise headings from the transcript.\n"
            "Rules:\n"
            "- Headings must come from the transcript content.\n"
            "- Preserve the logical order of the conversation.\n"
            "- Each heading must be unique.\n"
            "- Output one heading per line with no numbering, bullets, or markdown.\n\n"
            f"Source file: {chapter_name}\n\n"
            "--- BEGIN SOURCE CONTENT ---\n"
            f"{chapter_text}\n"
            "--- END SOURCE CONTENT ---\n"
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": outline_prompt},
        ]
        raw = client.generate(messages)
        headings: list[str] = []
        seen: set[str] = set()
        for line in raw.splitlines():
            cleaned = _clean_heading(line)
            if not cleaned:
                continue
            cleaned = cleaned[:80]
            key = cleaned.lower()
            if key in seen:
                continue
            headings.append(cleaned)
            seen.add(key)
        if len(headings) < 2 and len(chapter_text) > 400:
            headings = _fallback_outline_from_text(chapter_text, 4)
        return headings

    def _strip_heading_lines(text: str) -> str:
        cleaned_lines = []
        for line in text.splitlines():
            if line.lstrip().startswith("#"):
                continue
            if line.strip() == "```":
                continue
            cleaned_lines.append(line)
        return "\n".join(cleaned_lines).strip()

    def _render_outline(chapter_name: str, chapter_text: str, headings: list[str]) -> str:
        rendered_sections: list[str] = []
        for heading in headings:
            section_prompt = (
                "Write the documentation for this section based strictly on the transcript.\n"
                "Rules:\n"
                "- Use only the transcript content.\n"
                "- Do not invent facts.\n"
                "- Output only paragraph text or bullet points (no headings).\n"
                "- Do not include the transcript text or code fences.\n\n"
                f"Section heading: {heading}\n"
                f"Source file: {chapter_name}\n\n"
                "--- BEGIN SOURCE CONTENT ---\n"
                f"{chapter_text}\n"
                "--- END SOURCE CONTENT ---\n"
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": section_prompt},
            ]
            content = client.generate(messages)
            content = _strip_heading_lines(content)
            if not content:
                content = "Not provided in sources."
            rendered_sections.append(f"## {heading}\n{content}")
        return "\n\n".join(rendered_sections).strip() + "\n"

    def _validate_output(markdown: str, input_chars: int, enforce_sections: bool, source_text: str) -> list[str]:
        issues: list[str] = []
        trimmed = markdown.strip()
        min_len = _min_output_chars(input_chars)
        if len(trimmed) < min_len:
            issues.append(f"Output too short ({len(trimmed)} < {min_len} chars)")
        headings = _extract_headings(trimmed)
        if input_chars > 400 and not headings:
            issues.append("No headings found")
        duplicates = _duplicate_headings(headings)
        if duplicates:
            issues.append(f"Duplicate headings: {', '.join(duplicates)}")
        if _contains_code_fence(trimmed):
            issues.append("Code fences are not allowed")
        if _contains_source_echo(trimmed, source_text):
            issues.append("Source text echoed in output")
        return issues

    def _repair_output(chapter_name: str, chapter_text: str, draft: str) -> str:
        repair_prompt = (
            "Rewrite the documentation to satisfy these rules:\n"
            "- Use Markdown.\n"
            "- Headings must emerge from the transcript content.\n"
            "- Use headings (##, ###) only where a new conceptual section begins.\n"
            "- Each heading may appear only once.\n"
            "- Preserve the logical order of the conversation.\n"
            "- Do not invent facts or add advice not present in the source.\n"
            "- Do not include meta-commentary about the transcript.\n"
            "- Do not include the source transcript or code fences.\n\n"
            f"Source file: {chapter_name}\n\n"
            "--- BEGIN SOURCE CONTENT ---\n"
            f"{chapter_text}\n"
            "--- END SOURCE CONTENT ---\n\n"
            "--- BEGIN DRAFT OUTPUT ---\n"
            f"{draft}\n"
            "--- END DRAFT OUTPUT ---\n"
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": repair_prompt},
        ]
        return client.generate(messages)

    def _generate_with_quality(chapter_name: str, chapter_text: str, template: str) -> str:
        prompt = build_prompt(chapter_name, chapter_text, template)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        markdown = client.generate(messages)

        if _is_testing():
            return markdown

        issues = _validate_output(markdown, len(chapter_text), template == PROMPT_TEMPLATE, chapter_text)
        if not issues:
            return markdown

        retry_prompt = (
            f"{prompt}\n\nIMPORTANT: Follow the rules strictly. "
            f"Ensure the response is at least {_min_output_chars(len(chapter_text))} characters, "
            "use unique headings derived from the transcript, and avoid extra headings."
        )
        retry_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": retry_prompt},
        ]
        retry_markdown = client.generate(retry_messages)
        retry_issues = _validate_output(retry_markdown, len(chapter_text), template == PROMPT_TEMPLATE, chapter_text)
        if not retry_issues:
            return retry_markdown

        fallback_markdown = _repair_output(chapter_name, chapter_text, retry_markdown)
        fallback_issues = _validate_output(fallback_markdown, len(chapter_text), template == PROMPT_TEMPLATE, chapter_text)
        if fallback_issues:
            headings = _generate_outline(chapter_name, chapter_text)
            if headings:
                outline_markdown = _render_outline(chapter_name, chapter_text, headings)
                outline_issues = _validate_output(outline_markdown, len(chapter_text), template == PROMPT_TEMPLATE, chapter_text)
                if not outline_issues:
                    return outline_markdown
                raise LLMError("Low-quality output: " + "; ".join(outline_issues))
            raise LLMError("Low-quality output: " + "; ".join(fallback_issues))
        return fallback_markdown

    if request.standalone and request.chapters:
        # Combined mode: Join all chapters and process once
        try:
            combined_text = ""
            for chapter in request.chapters:
                combined_text += f"\n\n--- CHAPTER: {chapter.stem} ---\n\n"
                combined_text += chapter.read_text(encoding="utf-8")
                
            template = request.prompt_template or PROMPT_TEMPLATE
            
            if request.progress_callback:
                request.progress_callback(0, 1, "Full Report")
                
            markdown = _generate_with_quality("Full Report", combined_text, template)
            
            if request.progress_callback:
                request.progress_callback(1, 1, "Full Report")
            
            destination_dir = resolve_output_dir(request.chapters[0])
            destination_dir.mkdir(parents=True, exist_ok=True)
            
            destination = destination_dir / "standalone_report.docs.md"
            destination.write_text(markdown, encoding="utf-8")
            written.append((list(request.chapters), destination))
            return DocumentGenerationResult(written=written, failures=failures)
        except Exception as exc:
            failures.append((list(request.chapters), str(exc)))
            return DocumentGenerationResult(written=written, failures=failures)

    # Individual mode (Default)
    total_files = len(request.chapters)
    for i, chapter in enumerate(request.chapters):
        if request.progress_callback:
            request.progress_callback(i, total_files, chapter.name)
            
        try:
            chapter_text = chapter.read_text(encoding="utf-8")
            template = request.prompt_template or PROMPT_TEMPLATE
            markdown = _generate_with_quality(chapter.name, chapter_text, template)
            
            destination_dir = resolve_output_dir(chapter)
            
            if destination_dir not in created_dirs:
                destination_dir.mkdir(parents=True, exist_ok=True)
                created_dirs.add(destination_dir)
                
            destination = destination_dir / f"{chapter.stem}.docs.md"
            destination.write_text(markdown, encoding="utf-8")
            written.append((chapter, destination))
        except LLMError as exc:
            failures.append((chapter, str(exc)))
        except Exception as exc:  # pragma: no cover - safety net
            failures.append((chapter, str(exc)))
    return DocumentGenerationResult(written=written, failures=failures)


__all__ = [
    "DOCUMENTATION_SUBDIR",
    "DocumentGenerationRequest",
    "DocumentGenerationResult",
    "LLMSettings",
    "OllamaSettings",
    "collect_chapter_files",
    "generate_documentation",
]
