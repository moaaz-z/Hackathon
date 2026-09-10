import pytest
from fastapi.testclient import TestClient

from hackathon.api import repository as repository_api
from hackathon.main import app
from hackathon.services.ai_service import AIServiceError
from hackathon.services.github_service import (
    InvalidRepositoryUrlError,
    RepositoryCloneError,
    validate_github_url,
)
from tests.test_ai_service import VALID_REPORT

client = TestClient(app)

FACTS = {"statistics": {"total_files": 1}, "important_files": []}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/owner/repo",
        "https://github.com/owner/repo.git",
        "https://github.com/owner/repo/",
        "https://github.com/owner-name/repo.name",
    ],
)
def test_valid_github_urls_accepted(url):
    assert validate_github_url(url) == url.strip()


@pytest.mark.parametrize(
    "url",
    [
        "http://github.com/owner/repo",
        "https://gitlab.com/owner/repo",
        "https://github.com/owner",
        "git@github.com:owner/repo.git",
        "https://github.com/owner/repo/tree/main/src",
        "not a url",
        "",
    ],
)
def test_invalid_github_urls_rejected(url):
    with pytest.raises(InvalidRepositoryUrlError):
        validate_github_url(url)


def _patch_pipeline(monkeypatch, *, clone=None, analyze=None, ai=None, cleanup=None):
    cleaned: list[str] = []

    monkeypatch.setattr(
        repository_api, "clone_repository", clone or (lambda url: "/tmp/fake-repo")
    )
    monkeypatch.setattr(
        repository_api, "run_static_analysis", analyze or (lambda path: FACTS)
    )
    monkeypatch.setattr(
        repository_api, "generate_report", ai or (lambda facts: VALID_REPORT)
    )
    monkeypatch.setattr(
        repository_api,
        "cleanup_repository",
        cleanup or (lambda path: cleaned.append(path)),
    )
    return cleaned


def test_analyze_returns_facts_and_ai_review(monkeypatch):
    cleaned = _patch_pipeline(monkeypatch)

    response = client.post(
        "/repository/analyze", json={"url": "https://github.com/owner/repo"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["repository_url"] == "https://github.com/owner/repo"
    assert body["static_analysis"] == FACTS
    assert body["ai_review"]["health_score"] == 72
    assert body["ai_review"]["issues"][0]["severity"] == "high"
    assert cleaned == ["/tmp/fake-repo"], "temp clone was not cleaned up"


def test_invalid_url_returns_400(monkeypatch):
    _patch_pipeline(monkeypatch)

    response = client.post("/repository/analyze", json={"url": "https://gitlab.com/a/b"})

    assert response.status_code == 400
    assert "GitHub" in response.json()["detail"]


def test_clone_failure_returns_400(monkeypatch):
    def _fail(url):
        raise RepositoryCloneError("Could not clone repository.")

    _patch_pipeline(monkeypatch, clone=_fail)

    response = client.post(
        "/repository/analyze", json={"url": "https://github.com/owner/missing"}
    )

    assert response.status_code == 400
    assert "clone" in response.json()["detail"].lower()


def test_ai_failure_returns_502_and_cleans_up(monkeypatch):
    def _fail(facts):
        raise AIServiceError("The AI provider request failed.")

    cleaned = _patch_pipeline(monkeypatch, ai=_fail)

    response = client.post(
        "/repository/analyze", json={"url": "https://github.com/owner/repo"}
    )

    assert response.status_code == 502
    assert cleaned == ["/tmp/fake-repo"]


def test_unexpected_error_returns_generic_500(monkeypatch):
    def _boom(path):
        raise ValueError("internal detail that should not leak")

    cleaned = _patch_pipeline(monkeypatch, analyze=_boom)

    response = client.post(
        "/repository/analyze", json={"url": "https://github.com/owner/repo"}
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Analysis failed."
    assert "internal detail" not in response.text
    assert cleaned == ["/tmp/fake-repo"]


def test_missing_url_field_returns_422():
    response = client.post("/repository/analyze", json={})
    assert response.status_code == 422
