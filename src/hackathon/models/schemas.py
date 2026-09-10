from typing import Any, Literal

from pydantic import BaseModel, Field


class RepositoryAnalyzeRequest(BaseModel):
    url: str = Field(..., description="Public GitHub repository URL, e.g. https://github.com/owner/repo")


class Issue(BaseModel):
    severity: Literal["critical", "high", "medium", "low"]
    title: str
    file: str
    evidence: str
    recommendation: str


class AIReport(BaseModel):
    project_purpose: str
    summary: str
    technology_stack: list[str]
    architecture: str
    key_components: list[str]
    strengths: list[str]
    weaknesses: list[str]
    risks: list[str]
    recommendations: list[str]
    issues: list[Issue]
    health_score: int = Field(ge=0, le=100)
    final_assessment: str


class RepositoryAnalyzeResponse(BaseModel):
    repository_url: str
    static_analysis: dict[str, Any]
    ai_review: AIReport
