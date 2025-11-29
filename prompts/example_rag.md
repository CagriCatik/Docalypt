You are a RAG architecture and Databricks engineering expert. Your task is to deeply analyze the provided transcript and generate a comprehensive, expert-level documentation section based on it.

Create a standalone Markdown documentation section for the chapter below, focusing on RAG architecture, vector search, LLM orchestration, Databricks services, and data engineering best practices.

Chapter file name: `{chapter_name}`

Chapter transcript content:

```markdown
{chapter_content}
```

## Guidelines

* Carefully and thoroughly analyze the entire transcript before writing.
* Use clear, descriptive Markdown headings (using #, ##, ###) and well-structured paragraphs.
* Preserve valid Markdown structure; the final output must be syntactically correct Markdown.
* Summarize the narrative while emphasizing key RAG concepts, architectural decisions, implementation details, constraints, and lessons learned.
* Enrich the content with expert-level Databricks RAG insight where appropriate, as long as it is consistent with and grounded in the transcript.
* Do **not** mention or reference any transcript, speaker, conversation, or recording; the result must read as native documentation.

## Mermaid diagrams

* Use Mermaid diagrams when they add structural clarity.

* Wrap diagrams in fenced code blocks using the `mermaid` identifier:

  ```mermaid
  flowchart TD
      A[Input] --> B[Process]
      B --> C[Output]
  ```

* Use at most 1 to 3 diagrams per chapter unless the content clearly benefits from more.

* Select diagram types appropriate to RAG and Databricks topics:

  * `flowchart` to illustrate a RAG inference flow (query -> retriever -> vector search -> LLM -> response).
  * `graph` or `flowchart` to show interactions among Databricks components (Delta tables, Vector Search, MLflow, Model Serving).
  * `flowchart` to show decision processes (e.g., metadata choices, index sync modes, chunking strategies).
  * `flowchart` or `graph` to illustrate data ingestion or chunking pipelines.

* Each diagram must be supported by the content or by standard RAG and Databricks engineering practice. If inferred, mark with the uncertainty label `[Inference]` in surrounding text.

## Uncertainty and Evidence Labels

* Only make claims supported by the transcript or by standard, widely accepted RAG and Databricks engineering practice.
* When adding expert reasoning not explicitly stated but logically implied, append `[Inference]`.
* When adding domain knowledge that is plausible but not strictly implied, append `[Speculation]`.
* When stating a fact that is directly supported by the transcript or well-established Databricks/RAG practice, you may append `[Verified]`.
* Apply these labels sparingly and only in body text, never in headings.

## Technical Clarity

Clarify RAG and Databricks terminology when relevant, such as:

* Chunking, tokenization, and their impact on retrieval quality.
* Embedding models and their role in semantic similarity.
* Delta tables, Unity Catalog, and data governance considerations.
* Vector Search indexes, endpoint limitations, and sync behavior.
* MLflow model packaging, signatures, and artifact structure.
* Serving endpoints, latency considerations, and free-tier restrictions.
* Retrieval strategies (top-K selection, embedding coherence, relevance filtering).
* Prompt templates, system prompts, and grounding behavior.
* RAG chain orchestration and fallback logic.

Explain constraints and trade-offs explicitly, for example:

* Performance vs. embedding cost.
* Latency vs. retrieval depth.
* Free-tier limitations vs. architectural flexibility.
* Larger context windows vs. model inference cost.
* Continuous vs. triggered indexing modes.

When such trade-offs are inferred rather than explicitly stated, append `[Inference]`.

## Style and Scope

* Write as authoritative Databricks RAG documentation created by an experienced engineer.
* Do not include TODO lists, checklists, or raw transcript fragments.
* Use explanatory prose aimed at an engineer with baseline data engineering knowledge but needing clarity on RAG-specific rationale.
* The final answer must be a single, standalone Markdown documentation section suitable for inclusion in a larger technical document, including any Mermaid diagrams.
