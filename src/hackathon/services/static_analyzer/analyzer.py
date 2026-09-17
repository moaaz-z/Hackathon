from dataclasses import asdict
from typing import Any

from hackathon.services.static_analyzer.c_analyzer import analyze_c_files
from hackathon.services.static_analyzer.complexity import analyze_complexity
from hackathon.services.static_analyzer.dependencies import collect_dependencies
from hackathon.services.static_analyzer.frameworks import detect_frameworks
from hackathon.services.static_analyzer.importance import select_important_files
from hackathon.services.static_analyzer.python_analyzer import analyze_python_files
from hackathon.services.static_analyzer.relationships import build_relationships
from hackathon.services.static_analyzer.scanner import scan_repository
from hackathon.services.static_analyzer.snippets import extract_snippets
from hackathon.services.static_analyzer.tests import detect_tests


def _build_statistics(
    files,
    directory_count: int,
    python_function_count: int,
    python_class_count: int,
    c_function_count: int,
    c_header_count: int,
) -> dict[str, Any]:
    languages: dict[str, dict[str, int]] = {}
    total_loc = 0
    source_loc = 0
    source_files = 0

    for file_info in files:
        total_loc += file_info.loc

        if file_info.language is None:
            continue

        source_loc += file_info.loc
        source_files += 1

        bucket = languages.setdefault(
            file_info.language,
            {"files": 0, "loc": 0},
        )
        bucket["files"] += 1
        bucket["loc"] += file_info.loc

    languages = dict(
        sorted(
            languages.items(),
            key=lambda item: item[1]["loc"],
            reverse=True,
        )
    )

    dominant_language = next(iter(languages), None)

    return {
        "total_files": len(files),
        "source_files": source_files,
        "total_directories": directory_count,
        "total_loc": total_loc,
        "source_loc": source_loc,
        "languages": languages,
        "dominant_language": dominant_language,
        "function_count": python_function_count + c_function_count,
        "python_function_count": python_function_count,
        "python_class_count": python_class_count,
        "c_function_count": c_function_count,
        "c_header_count": c_header_count,
        "function_count_languages": ["Python", "C"],
    }


def _build_quality(
    complexity: dict[str, Any],
    tests: dict[str, Any],
    has_readme: bool,
) -> dict[str, Any]:
    function_complexities = [
        entry["complexity"]
        for entry in complexity["python_function_complexity"]
    ]

    average_complexity = (
        round(
            sum(function_complexities) / len(function_complexities),
            2,
        )
        if function_complexities
        else 0.0
    )

    return {
        "has_readme": has_readme,
        "average_python_function_complexity": average_complexity,
        "python_complexity_available": bool(function_complexities),
        "todo_fixme_count": len(complexity["todo_fixme_markers"]),
        "large_file_count": len(complexity["large_files"]),
        "test_file_ratio": tests["test_file_ratio"],
    }


def analyze_repository(repo_path: str) -> dict[str, Any]:
    scan_result = scan_repository(repo_path)
    files = scan_result.files

    python_files = [
        file_info
        for file_info in files
        if file_info.language == "Python"
    ]

    c_files = [
        file_info
        for file_info in files
        if file_info.language == "C"
    ]

    python_facts = analyze_python_files(python_files)
    c_facts = analyze_c_files(c_files)

    dependencies = collect_dependencies(
        repo_path,
        scan_result.config_files,
    )
    frameworks = detect_frameworks(dependencies)
    tests = detect_tests(files)
    complexity = analyze_complexity(python_files, files)

    relationships = build_relationships(
        python_facts.imports,
        python_files,
    )

    important_files = select_important_files(
        files,
        relationships,
        complexity,
    )

    snippets = extract_snippets(
        repo_path,
        important_files,
    )

    quality = _build_quality(
        complexity,
        tests,
        scan_result.readme_path is not None,
    )

    statistics = _build_statistics(
        files=files,
        directory_count=scan_result.directory_count,
        python_function_count=len(python_facts.functions),
        python_class_count=len(python_facts.classes),
        c_function_count=len(c_facts["functions"]),
        c_header_count=c_facts["header_file_count"],
    )

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
        "c": c_facts,
        "dependencies": dependencies,
        "frameworks": frameworks,
        "tests": tests,
        "complexity": complexity,
        "quality": quality,
        "relationships": relationships,
        "important_files": important_files,
        "snippets": snippets,
    }
