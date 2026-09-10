from dataclasses import asdict
from typing import Any

from hackathon.services.static_analyzer.complexity import analyze_complexity
from hackathon.services.static_analyzer.dependencies import collect_dependencies
from hackathon.services.static_analyzer.frameworks import detect_frameworks
from hackathon.services.static_analyzer.importance import select_important_files
from hackathon.services.static_analyzer.python_analyzer import analyze_python_files
from hackathon.services.static_analyzer.relationships import build_relationships
from hackathon.services.static_analyzer.scanner import scan_repository
from hackathon.services.static_analyzer.snippets import extract_snippets
from hackathon.services.static_analyzer.tests import detect_tests


def _build_statistics(files, directory_count: int) -> dict[str, Any]:
    languages: dict[str, dict[str, int]] = {}
    total_loc = 0

    for file_info in files:
        total_loc += file_info.loc
        if file_info.language is None:
            continue
        bucket = languages.setdefault(file_info.language, {"files": 0, "loc": 0})
        bucket["files"] += 1
        bucket["loc"] += file_info.loc

    return {
        "total_files": len(files),
        "total_directories": directory_count,
        "total_loc": total_loc,
        "languages": dict(sorted(languages.items(), key=lambda item: item[1]["loc"], reverse=True)),
    }


def _build_quality(complexity: dict[str, Any], tests: dict[str, Any], has_readme: bool) -> dict[str, Any]:
    function_complexities = [entry["complexity"] for entry in complexity["python_function_complexity"]]
    average_complexity = round(sum(function_complexities) / len(function_complexities), 2) if function_complexities else 0.0

    return {
        "has_readme": has_readme,
        "average_python_function_complexity": average_complexity,
        "todo_fixme_count": len(complexity["todo_fixme_markers"]),
        "large_file_count": len(complexity["large_files"]),
        "test_file_ratio": tests["test_file_ratio"],
    }


def analyze_repository(repo_path: str) -> dict[str, Any]:
    scan_result = scan_repository(repo_path)
    files = scan_result.files
    python_files = [f for f in files if f.language == "Python"]

    python_facts = analyze_python_files(python_files)
    dependencies = collect_dependencies(repo_path, scan_result.config_files)
    frameworks = detect_frameworks(dependencies)
    tests = detect_tests(files)
    complexity = analyze_complexity(python_files, files)
    relationships = build_relationships(python_facts.imports, python_files)
    important_files = select_important_files(files, relationships, complexity)
    snippets = extract_snippets(repo_path, important_files)
    quality = _build_quality(complexity, tests, scan_result.readme_path is not None)
    statistics = _build_statistics(files, scan_result.directory_count)

    return {
        "statistics": statistics,
        "languages": statistics["languages"],
        "structure": {
            "has_readme": scan_result.readme_path is not None,
            "readme_path": scan_result.readme_path,
            "config_files": scan_result.config_files,
        },
        "python": {
            "functions": [asdict(f) for f in python_facts.functions],
            "classes": [asdict(c) for c in python_facts.classes],
            "imports": [asdict(i) for i in python_facts.imports],
            "parse_errors": python_facts.parse_errors,
        },
        "dependencies": dependencies,
        "frameworks": frameworks,
        "tests": tests,
        "complexity": complexity,
        "quality": quality,
        "relationships": relationships,
        "important_files": important_files,
        "snippets": snippets,
    }
