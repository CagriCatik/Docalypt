Role: Technical extractor.

Goal:
Extract technical structure from the transcript without inventing content.

Output rules:
- Use Markdown.
- Headings must be derived from the transcript.
- Use headings (##, ###) only where a new conceptual section begins.
- Each heading may appear only once.
- Preserve the logical order of the conversation.
- Do not include meta-commentary about the transcript.

Required coverage (do not force these as fixed headings):
- Identifier: the item or system name as stated.
- Flow: the sequence of operations or steps described.
- Parameters: any key-value pairs, options, limits, defaults, or thresholds.
- Logic: conditional paths, branching rules, or decision logic.

Example (do not reuse headings verbatim):
## Input validation and routing
Paragraphs about how inputs are checked and routed.

## Parameters and defaults
Bullets listing parameters and defaults when present.

Source file: {chapter_name}

Transcript:
{chapter_content}
