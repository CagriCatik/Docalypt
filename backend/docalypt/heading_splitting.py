import re
from pathlib import Path
from typing import List, Dict, Optional

def split_by_headings(
    file_path: Path,
    output_dir: Path,
    base_dir: Optional[Path] = None,
) -> List[Dict[str, str]]:
    """Splits a markdown file by headings or smart markers (like [Music])."""
    content = file_path.read_text(encoding="utf-8")
    
    # Try heading split first
    header_pattern = re.compile(r"^(#{1,2})\s+(.+)$", re.MULTILINE)
    headers = list(header_pattern.finditer(content))
    
    chunks = []
    if headers:
        last_pos = 0
        for i, match in enumerate(headers):
            title = match.group(2).strip()
            # Start of next header or end of file
            next_start = headers[i+1].start() if i + 1 < len(headers) else len(content)
            chunk_text = content[match.start():next_start].strip()
            chunks.append({"title": title, "text": chunk_text})
    else:
        # No headings? Try splitting by [Music] markers anywhere
        # We split the text and then reconstruct chapters
        raw_chunks = re.split(r"\[Music\]", content, flags=re.IGNORECASE)
        for i, chunk in enumerate(raw_chunks):
            text = chunk.strip()
            if not text:
                continue
            
            # Create a title from the first line or first 5 words
            first_line = text.splitlines()[0] if text.splitlines() else "Untitled"
            title = " ".join(first_line.split()[:6]) + "..." if len(first_line.split()) > 6 else first_line
            chunks.append({"title": title, "text": text})

    output_dir.mkdir(parents=True, exist_ok=True)
    written_files = []
    
    for i, chapter in enumerate(chunks, 1):
        slug = re.sub(r"[^\w-]", "_", chapter["title"].lower().replace(" ", "_"))
        filename = f"{i:02d}_{slug}.md"
        dest = output_dir / filename
        dest.write_text(chapter["text"] + "\n", encoding="utf-8")
        rel_path = dest
        if base_dir is not None:
            try:
                rel_path = dest.relative_to(base_dir)
            except ValueError:
                rel_path = dest
        written_files.append({
            "title": f"{i}. {chapter['title']}", 
            "filename": filename, 
            "path": rel_path.as_posix()
        })
        
    return written_files
