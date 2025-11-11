"""Application service orchestrating documentation generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from docalypt.domain.models import DocumentJob, DocumentOutcome

from .protocols import DocumentationGateway


@dataclass(slots=True)
class GenerateDocumentationUseCase:
    """Generate documentation for a set of chapters via a gateway."""

    gateway: DocumentationGateway

    def execute(
        self,
        chapters: Sequence[Path],
        destination_dirname: str,
        prompt_template: str | None = None,
    ) -> DocumentOutcome:
        job = DocumentJob(
            chapters=chapters,
            destination_dirname=destination_dirname,
            prompt_template=prompt_template,
        )
        return self.gateway.generate_documents(
            job_chapters=job.chapters,
            destination_dirname=job.destination_dirname,
            prompt_template=job.prompt_template,
        )


__all__ = ["GenerateDocumentationUseCase"]
