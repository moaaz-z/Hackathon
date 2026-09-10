import json

import pytest

from hackathon.models.schemas import AIReport
from hackathon.services import ai_service
from hackathon.services.ai_service import AIServiceError, generate_report

VALID_REPORT = {
    "project_purpose": "A sample service.",
    "summary": "Small FastAPI app.",
    "technology_stack": ["Python", "FastAPI"],
    "architecture": "Layered API.",
    "key_components": ["api", "services"],
    "strengths": ["Modular"],
    "weaknesses": ["No tests"],
    "risks": ["Unvalidated input"],
    "recommendations": ["Add tests"],
    "issues": [
        {
            "severity": "high",
            "title": "Missing tests",
            "file": "src/sample/main.py",
            "evidence": "test_file_ratio is 0.0",
            "recommendation": "Add pytest coverage.",
        }
    ],
    "health_score": 72,
    "final_assessment": "Reasonable MVP.",
}


class _FakeResponse:
    def __init__(self, text: str) -> None:
        self.text = text


class _FakeModels:
    def __init__(self, text: str, recorder: dict) -> None:
        self._text = text
        self._recorder = recorder

    def generate_content(self, **kwargs):
        self._recorder.update(kwargs)
        return _FakeResponse(self._text)


class _FakeClient:
    def __init__(self, text: str, recorder: dict) -> None:
        self.models = _FakeModels(text, recorder)


@pytest.fixture
def fake_gemini(monkeypatch):
    recorder: dict = {}

    def _install(text: str = json.dumps(VALID_REPORT)):
        monkeypatch.setattr(
            ai_service.genai,
            "Client",
            lambda api_key=None: _FakeClient(text, recorder),
        )
        return recorder

    monkeypatch.setenv("GEMINI_API_KEY", "test-key-not-real")
    return _install


def test_missing_api_key_raises_clear_error(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(AIServiceError, match="GEMINI_API_KEY"):
        generate_report({"statistics": {}})


def test_generate_report_returns_structured_json(fake_gemini):
    fake_gemini()
    report = generate_report({"statistics": {"total_files": 3}})

    assert report["health_score"] == 72
    assert report["issues"][0]["severity"] == "high"
    # Must be JSON-serialisable for direct React consumption.
    json.dumps(report)


def test_request_sends_evidence_and_json_schema(fake_gemini):
    recorder = fake_gemini()
    facts = {"statistics": {"total_files": 3}}
    generate_report(facts)

    assert recorder["config"].response_mime_type == "application/json"
    assert recorder["config"].response_json_schema == AIReport.model_json_schema()

    contents = "\n".join(recorder["contents"])
    assert "senior software architect" in contents
    assert "do not invent information" in contents
    assert json.dumps(facts, default=str) in contents


def test_empty_response_raises(fake_gemini):
    fake_gemini(text="")

    with pytest.raises(AIServiceError, match="empty"):
        generate_report({"statistics": {}})


def test_provider_failure_does_not_leak_details(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-not-real")

    class _ExplodingModels:
        def generate_content(self, **kwargs):
            raise RuntimeError("upstream 400: key=test-key-not-real leaked")

    class _ExplodingClient:
        def __init__(self) -> None:
            self.models = _ExplodingModels()

    monkeypatch.setattr(ai_service.genai, "Client", lambda api_key=None: _ExplodingClient())

    with pytest.raises(AIServiceError) as excinfo:
        generate_report({"statistics": {}})

    assert "test-key-not-real" not in str(excinfo.value)


def test_invalid_severity_is_rejected(fake_gemini):
    bad = dict(VALID_REPORT)
    bad["issues"] = [dict(VALID_REPORT["issues"][0], severity="catastrophic")]
    fake_gemini(text=json.dumps(bad))

    with pytest.raises(Exception):
        generate_report({"statistics": {}})


def test_health_score_out_of_range_is_rejected(fake_gemini):
    bad = dict(VALID_REPORT, health_score=140)
    fake_gemini(text=json.dumps(bad))

    with pytest.raises(Exception):
        generate_report({"statistics": {}})
