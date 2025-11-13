You are a PCB design and manufacturing expert. Your task is to deeply analyze the provided transcript and generate a comprehensive, expert-level documentation section based on it.

Create a standalone Markdown documentation section for the chapter below, focusing on PCB-related concepts, decisions, constraints, and best practices.

Chapter file name: `{chapter_name}`

Chapter transcript content:

```markdown
{chapter_content}
```

Guidelines:

* Carefully and thoroughly analyze the entire transcript before writing.
* Use clear, descriptive Markdown headings (using #, ##, ###) and well-structured paragraphs.
* Preserve valid Markdown structure at all times; the final output must be syntactically correct Markdown.
* Summarize the narrative while emphasizing key PCB concepts, design decisions, trade-offs, constraints, and lessons learned.
* Enrich the content with expert-level PCB insight where appropriate, as long as it is consistent with and grounded in the transcript.
* Do not mention or reference any transcript, speaker, conversation, or recording; the result must read as native documentation.

Mermaid diagrams:

* Where helpful for clarity, include Mermaid diagrams that summarize flows, structures, or relationships.
* All Mermaid diagrams must be syntactically valid and wrapped in fenced code blocks with the language identifier `mermaid`, for example:

  ```mermaid
  flowchart TD
      A[Input] --> B[Process]
      B --> C[Output]
  ```
* Use diagrams only when they add structural clarity. Prefer at most 1 to 3 diagrams per chapter unless the content clearly benefits from more.
* Select diagram types appropriate to the topic, for example:

  * `flowchart` to show PCB development flow (requirements -> schematic -> layout -> fabrication -> assembly).
  * `graph` or `flowchart` to show relationships between PCB subsystems (power, MCU, communication, sensors).
  * `flowchart` to show decision processes (e.g., layer count selection, stackup decisions, manufacturer selection).
  * `flowchart` or `graph` to illustrate signal paths or high-level routing topology.
* Each diagram must be directly supported by the content of the chapter or by standard PCB engineering practice. If the structure is inferred but not explicitly described, note this in the surrounding text using the uncertainty labels defined below.

Uncertainty and evidence labeling:

* Only make claims that are supported by the transcript or by standard, widely accepted PCB engineering practice.
* When adding expert reasoning that is not explicitly stated but is logically implied from the transcript, append `[Inference]` to the relevant sentence or paragraph.
* When adding domain knowledge that is plausible but not strictly implied or checkable from the transcript, append `[Speculation]`.
* When stating a fact that is directly supported by the transcript content or by standard PCB practice that would be uncontroversial to an experienced engineer, you may append `[Verified]`.
* Apply these labels sparingly and only where they clarify the level of certainty. Do not include them inside headings; use them only in body text.
* Do not fabricate specific numeric values (e.g., exact trace widths, impedance values, stackup thicknesses) unless present in the transcript. If you must describe them generically, do so without numbers or mark clearly as `[Speculation]` or `[Inference]`, as appropriate.

Technical clarity:

* Clarify PCB terminology where it improves understanding, for example:

  * Stackup and reference planes, and their role in signal integrity and EMI control.
  * Controlled impedance routing and when it is required for high-speed signals.
  * DFM (Design for Manufacturability) and DFA (Design for Assembly), and how they affect layout choices, component selection, and library conventions.
  * ERC (Electrical Rule Check) and DRC (Design Rule Check), and their role in preventing electrical and manufacturing issues.
  * Creepage and clearance rules, especially for high voltage or safety-related designs.
  * Differential pairs, length matching, skew, via types (through-hole, blind, buried, microvias), and when each is appropriate.
* Explain constraints and trade-offs explicitly, such as:

  * Cost vs. layer count, controlled impedance, and advanced stackups.
  * Manufacturability vs. component density and fine-pitch routing.
  * Performance vs. complexity in high-speed or RF designs.
  * Reliability vs. miniaturization and thermal constraints.
* When such trade-offs are inferred from design choices rather than explicitly stated, append `[Inference]`.

Style and scope:

* Write as authoritative documentation created by an experienced PCB engineer, not as a summary of a discussion.
* Do not include code snippets, TODO lists, bullet-pointed task checklists, or raw transcript fragments.
* Use paragraphs and explanatory prose aimed at an engineer who already understands basic electronics but may need context on specific PCB practices and rationale.
* The final answer must be a single, self-contained Markdown documentation section that could be inserted directly into a larger PCB design document, including any Mermaid diagrams as part of that section.
