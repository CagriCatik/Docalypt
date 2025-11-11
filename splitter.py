
# File: splitter.py
from pathlib import Path
import re
from typing import Callable, Optional, List, Tuple

from config import load_config


def parse_hhmmss(ts: str) -> int:
    """
    Convert 'MM:SS' or 'HH:MM:SS' into total seconds.
    """
    parts = list(map(int, ts.split(':')))
    if len(parts) == 2:
        hours, minutes, seconds = 0, parts[0], parts[1]
    else:
        hours, minutes, seconds = parts
    return hours * 3600 + minutes * 60 + seconds


class TranscriptSplitter:
    """
    Splits a markdown transcript into chapter files.

    Supports plugin hooks and HTML export.
    """
    def __init__(
        self,
        input_path: Path,
        output_dir: Optional[Path] = None,
        marker_regex: Optional[str] = None,
        on_progress: Optional[Callable[[int, int], None]] = None,
        pre_split_hooks: Optional[List[Callable[[str], str]]] = None,
        post_split_hooks: Optional[List[Callable[[Path], None]]] = None,
    ):
        cfg = load_config()
        self.input_path = input_path
        self.output_dir = output_dir or Path(cfg.get("output_dir"))
        self.marker_regex = re.compile(
            marker_regex or cfg.get("marker_regex")
        )
        self.on_progress = on_progress
        self.pre_split_hooks = pre_split_hooks or []
        self.post_split_hooks = post_split_hooks or []
        self.chapter_count = 0

    def split(self, export_html: bool = False) -> int:
        text = self.input_path.read_text(encoding='utf-8')
        header, body = text.split("\n\nTranscript:", 1)

        # 1) Parse chapter definitions
        chapters: List[Tuple[int, str]] = []
        for line in header.splitlines():
            m = re.match(r"^(\d{2}:\d{2}:\d{2})\s*[-–]\s*(.+)$", line)
            if m:
                ts, title = m.groups()
                chapters.append((parse_hhmmss(ts), title.strip()))
        chapters.sort(key=lambda x: x[0])
        times = [t for t, _ in chapters]
        titles = [t for _, t in chapters]

        # 2) Apply pre-split hooks to body
        for hook in self.pre_split_hooks:
            body = hook(body)

        # 3) Split transcript
        buckets = {title: [] for title in titles}
        parts = self.marker_regex.split(body)
        total = (len(parts) - 1) // 2
        idx = 0
        for i in range(1, len(parts), 2):
            idx += 1
            sec = parse_hhmmss(parts[i])
            snippet = parts[i + 1].strip()
            bucket = titles[max(j for j, t in enumerate(times) if t <= sec)]
            buckets[bucket].append(snippet)
            if self.on_progress:
                self.on_progress(idx, total)

        # 4) Ensure output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 5) Write files
        md_paths = []
        for i, (title, texts) in enumerate(buckets.items(), start=1):
            safe = re.sub(r"[^\w-]", "_", title.lower().replace(' ', '_'))
            fname = f"{i:02d}_{safe}.md"
            path = self.output_dir / fname
            content = f"# {title}\n\n" + "\n\n".join(texts)
            path.write_text(content, encoding='utf-8')
            md_paths.append(path)
            for hook in self.post_split_hooks:
                hook(path)

        self.chapter_count = len(md_paths)

        # 6) Optional HTML export
        if export_html:
            self._export_html(md_paths)

        return self.chapter_count

    def _export_html(self, md_paths: List[Path]) -> None:
        """
        Simple HTML export: concatenate all chapters into index.html
        """
        html_parts = ["<html><body><h1>Transcript Chapters</h1><ul>"]
        for md in md_paths:
            chapter_html = md.read_text(encoding='utf-8')
            # naive conversion (could use markdown lib)
            body = chapter_html.replace('# ', '<h2>').replace('\n\n', '</h2><p>')
            html_parts.append(f"<li>{body}</li>")
        html_parts.append('</ul></body></html>')
        html_file = self.output_dir / 'index.html'
        html_file.write_text(''.join(html_parts), encoding='utf-8')
