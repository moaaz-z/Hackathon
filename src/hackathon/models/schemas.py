from typing import Any

from pydantic import BaseModel, Field


class RepositoryAnalyzeRequest(BaseModel):
    url: str = Field(..., description="Public GitHub repository URL, e.g. https://github.com/owner/repo")


class RepositoryAnalyzeResponse(BaseModel):
    repository_url: str
    static_analysis: dict[str, Any]
    ai_review: dict[str, Any]
