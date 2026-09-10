from fastapi import APIRouter, HTTPException

from hackathon.models.schemas import RepositoryAnalyzeRequest, RepositoryAnalyzeResponse
from hackathon.services import ai_service_stub as ai_service
from hackathon.services import static_analyzer_stub as static_analyzer
from hackathon.services.github_service import (
    InvalidRepositoryUrlError,
    RepositoryCloneError,
    clone_repository,
    cleanup_repository,
    validate_github_url,
)

router = APIRouter(prefix="/repository", tags=["repository"])


@router.post("/analyze", response_model=RepositoryAnalyzeResponse)
def analyze_repository(request: RepositoryAnalyzeRequest) -> RepositoryAnalyzeResponse:
    try:
        url = validate_github_url(request.url)
    except InvalidRepositoryUrlError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        repo_path = clone_repository(url)
    except RepositoryCloneError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        static_analysis = static_analyzer.analyze(repo_path)
        ai_review = ai_service.generate_report(static_analysis)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Analysis failed.") from exc
    finally:
        cleanup_repository(repo_path)

    return RepositoryAnalyzeResponse(
        repository_url=url,
        static_analysis=static_analysis,
        ai_review=ai_review,
    )
