import os
import textwrap

from hackathon.services.static_analyzer import analyze_repository
from hackathon.services.static_analyzer.analyzer import analyze_repository as analyzer_entry


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content))


def _build_sample_repo(root: str) -> None:
    _write(f"{root}/README.md", "# Sample\n")
    _write(
        f"{root}/pyproject.toml",
        """
        [project]
        name = "sample"
        dependencies = ["fastapi>=0.100.0", "radon>=6.0.1"]
        """,
    )
    _write(
        f"{root}/package.json",
        '{"dependencies": {"react": "^18.0.0"}, "devDependencies": {"vitest": "^1.0.0"}}',
    )
    _write(
        f"{root}/src/sample/main.py",
        """
        from sample.services.helper import helper_function

        def main():
            return helper_function()
        """,
    )
    _write(
        f"{root}/src/sample/services/__init__.py",
        "",
    )
    _write(
        f"{root}/src/sample/services/helper.py",
        """
        import os

        # TODO: make this configurable
        class Helper:
            @staticmethod
            def run(value, flag=False):
                if flag and value > 3:
                    return os.sep
                return None

        def helper_function():
            return Helper.run(1)
        """,
    )
    _write(
        f"{root}/tests/test_helper.py",
        """
        def test_placeholder():
            assert True
        """,
    )
    # Should all be ignored by the scanner.
    _write(f"{root}/node_modules/pkg/index.js", "module.exports = 1;\n")
    _write(f"{root}/.venv/lib/thing.py", "x = 1\n")
    _write(f"{root}/dist/bundle.js", "var a = 1;\n")
    _write(f"{root}/logo.png", "not-really-an-image")


def test_analyze_repository_returns_all_fact_sections(tmp_path):
    _build_sample_repo(str(tmp_path))
    result = analyze_repository(str(tmp_path))

    for key in (
        "statistics",
        "languages",
        "structure",
        "python",
        "dependencies",
        "frameworks",
        "tests",
        "complexity",
        "quality",
        "relationships",
        "important_files",
        "snippets",
    ):
        assert key in result, f"missing fact section: {key}"


def test_public_entry_point_is_exported():
    assert analyze_repository is analyzer_entry


def test_ignores_generated_and_binary_paths(tmp_path):
    _build_sample_repo(str(tmp_path))
    result = analyze_repository(str(tmp_path))

    paths = {f for f in result["snippets"]}
    all_text = str(result)

    assert "node_modules" not in all_text
    assert ".venv" not in all_text
    assert "dist/bundle.js" not in all_text
    assert not any(p.endswith(".png") for p in paths)


def test_detects_languages_and_loc(tmp_path):
    _build_sample_repo(str(tmp_path))
    stats = analyze_repository(str(tmp_path))["statistics"]

    assert stats["total_files"] > 0
    assert stats["total_loc"] > 0
    assert "Python" in stats["languages"]
    assert stats["languages"]["Python"]["files"] >= 3


def test_detects_readme_and_config_files(tmp_path):
    _build_sample_repo(str(tmp_path))
    structure = analyze_repository(str(tmp_path))["structure"]

    assert structure["has_readme"] is True
    assert structure["readme_path"] == "README.md"
    assert "pyproject.toml" in structure["config_files"]
    assert "package.json" in structure["config_files"]


def test_extracts_python_functions_classes_and_imports(tmp_path):
    _build_sample_repo(str(tmp_path))
    python_facts = analyze_repository(str(tmp_path))["python"]

    function_names = {f["name"] for f in python_facts["functions"]}
    class_names = {c["name"] for c in python_facts["classes"]}
    modules = {i["module"] for i in python_facts["imports"]}

    assert "main" in function_names
    assert "helper_function" in function_names
    assert "Helper" in class_names
    assert "sample.services.helper" in modules
    assert python_facts["parse_errors"] == []

    helper_class = next(c for c in python_facts["classes"] if c["name"] == "Helper")
    assert "run" in helper_class["methods"]

    run_method = next(f for f in python_facts["functions"] if f["name"] == "run")
    assert run_method["is_method"] is True
    assert run_method["class_name"] == "Helper"
    assert "staticmethod" in run_method["decorators"]


def test_detects_dependencies_across_ecosystems(tmp_path):
    _build_sample_repo(str(tmp_path))
    dependencies = analyze_repository(str(tmp_path))["dependencies"]

    python_names = {d["name"] for d in dependencies["python"]}
    node_names = {d["name"] for d in dependencies["node"]}

    assert "fastapi" in python_names
    assert "radon" in python_names
    assert "react" in node_names
    assert "vitest" in node_names


def test_detects_frameworks_only_with_evidence(tmp_path):
    _build_sample_repo(str(tmp_path))
    frameworks = analyze_repository(str(tmp_path))["frameworks"]

    names = {f["name"] for f in frameworks}
    assert "FastAPI" in names
    assert "React" in names
    # No Django/Flask dependency exists, so they must not be claimed.
    assert "Django" not in names
    assert "Flask" not in names


def test_test_ratio_is_counted_without_claiming_coverage(tmp_path):
    _build_sample_repo(str(tmp_path))
    tests = analyze_repository(str(tmp_path))["tests"]

    assert "tests/test_helper.py" in tests["test_files"]
    assert tests["test_file_count"] == 1
    assert 0 < tests["test_file_ratio"] <= 1
    assert "coverage" in tests["note"].lower()


def test_complexity_and_todo_markers(tmp_path):
    _build_sample_repo(str(tmp_path))
    complexity = analyze_repository(str(tmp_path))["complexity"]

    assert complexity["python_function_complexity"]
    entry = complexity["python_function_complexity"][0]
    assert {"file", "name", "complexity", "rank", "lineno"} <= set(entry)

    markers = complexity["todo_fixme_markers"]
    assert any(m["marker"] == "TODO" for m in markers)
    assert isinstance(complexity["large_files"], list)


def test_resolves_internal_imports_in_src_layout(tmp_path):
    _build_sample_repo(str(tmp_path))
    relationships = analyze_repository(str(tmp_path))["relationships"]

    internal = relationships["internal_imports"]
    assert "src/sample/main.py" in internal, "src-layout import failed to resolve"
    assert "src/sample/services/helper.py" in internal["src/sample/main.py"]
    assert relationships["import_in_degree"]["src/sample/services/helper.py"] == 1


def test_resolves_relative_imports(tmp_path):
    root = str(tmp_path)
    _write(f"{root}/pkg/__init__.py", "")
    _write(f"{root}/pkg/target.py", "VALUE = 1\n")
    _write(f"{root}/pkg/consumer.py", "from .target import VALUE\n")

    relationships = analyze_repository(root)["relationships"]
    internal = relationships["internal_imports"]

    assert "pkg/target.py" in internal.get("pkg/consumer.py", [])


def test_important_files_are_ranked_and_bounded(tmp_path):
    _build_sample_repo(str(tmp_path))
    important = analyze_repository(str(tmp_path))["important_files"]

    assert important
    assert len(important) <= 20
    scores = [entry["score"] for entry in important]
    assert scores == sorted(scores, reverse=True)
    assert all(entry["reasons"] for entry in important)

    paths = {entry["path"] for entry in important}
    assert "src/sample/main.py" in paths


def test_size_alone_does_not_make_a_file_important():
    from hackathon.services.static_analyzer.importance import select_important_files
    from hackathon.services.static_analyzer.models import FileInfo

    # A large file with no entry point, keyword, import or complexity signal
    # must not be reported as important with an empty reason list.
    files = [
        FileInfo(
            path="data/generated_blob.json",
            absolute_path="/x/data/generated_blob.json",
            language="JSON",
            loc=5000,
            size_bytes=100000,
        )
    ]

    result = select_important_files(
        files, {"import_in_degree": {}}, {"python_function_complexity": []}
    )

    assert result == []


def test_readme_is_kept_as_purpose_evidence(tmp_path):
    _build_sample_repo(str(tmp_path))
    important = analyze_repository(str(tmp_path))["important_files"]

    readme = next((e for e in important if e["path"] == "README.md"), None)
    assert readme is not None
    assert "project README" in readme["reasons"]


def test_snippets_are_limited(tmp_path):
    _build_sample_repo(str(tmp_path))
    snippets = analyze_repository(str(tmp_path))["snippets"]

    assert snippets
    for content in snippets.values():
        assert len(content) <= 1500
        assert content.count("\n") <= 40


def test_quality_summary_fields(tmp_path):
    _build_sample_repo(str(tmp_path))
    quality = analyze_repository(str(tmp_path))["quality"]

    assert quality["has_readme"] is True
    assert quality["average_python_function_complexity"] >= 0
    assert quality["todo_fixme_count"] >= 1


def test_handles_unparsable_python_without_crashing(tmp_path):
    _write(f"{tmp_path}/broken.py", "def oops(:\n")
    result = analyze_repository(str(tmp_path))

    assert result["python"]["parse_errors"]
    assert "broken.py" in result["python"]["parse_errors"][0]


def test_handles_empty_repository(tmp_path):
    result = analyze_repository(str(tmp_path))

    assert result["statistics"]["total_files"] == 0
    assert result["structure"]["has_readme"] is False
    assert result["important_files"] == []
    assert result["tests"]["test_file_ratio"] == 0.0
