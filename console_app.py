import re
from datetime import timedelta
from collections import OrderedDict

def parse_hhmmss(ts):
    """Convert 'MM:SS' or 'HH:MM:SS' to total seconds."""
    parts = list(map(int, ts.split(":")))
    if len(parts) == 2:
        m, s = parts
        return m * 60 + s
    h, m, s = parts
    return h*3600 + m*60 + s

# 1. Load the full Markdown
with open("transcript.md", encoding="utf-8") as f:
    all_text = f.read().strip()

# 2. Split off the timestamp list vs. the transcript body
header, raw = all_text.split("\n\nTranscript:", 1)

# 3. Parse chapters from the header lines
chapters = []
for line in header.splitlines():
    m = re.match(r"^(\d{2}:\d{2}:\d{2})\s*[-–]\s*(.+)$", line.strip())
    if m:
        ts, title = m.groups()
        chapters.append((parse_hhmmss(ts), title.strip()))

# Sort by time
chapters.sort(key=lambda x: x[0])
times = [t for t, _ in chapters]
titles = [t for _, t in chapters]

# Prepare empty buckets
buckets = OrderedDict((title, []) for title in titles)

# 4. Split the transcript into (time, text) snippets
pattern = re.compile(r"\((\d{1,2}:\d{2}(?::\d{2})?)\)")
parts = pattern.split(raw)

snippets = []
for i in range(1, len(parts), 2):
    ts_str = parts[i]
    text = parts[i+1].strip()
    sec = parse_hhmmss(ts_str)
    snippets.append((sec, text))

# 5. Assign each snippet to its chapter
for sec, text in snippets:
    idx = max(i for i, t in enumerate(times) if t <= sec)
    buckets[titles[idx]].append(text)

# 6. Write out each chapter as its own numbered .md file
for idx, (title, texts) in enumerate(buckets.items(), start=1):
    # zero-pad the index, sanitize filename
    num = f"{idx:02d}"
    safe = title.lower().replace(" ", "_").replace("/", "_")
    fname = f"{num}_{safe}.md"
    with open(fname, "w", encoding="utf-8") as out:
        out.write(f"# {title}\n\n")
        out.write("\n\n".join(texts))

print("Done! Your Markdown has been split into numbered chapter files.")
