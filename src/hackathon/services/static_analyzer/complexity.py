import re

from radon.complexity import cc_rank, cc_visit
from radon.visitors import Function

from hackathon.services.static_analyzer.constants import LARGE_FILE_LOC_THRESHOLD
from hackathon.services.static_analyzer.models import FileInfo

_TODO_PATTERN = re.compile(r"\b(TODO|FIXME)\b[:\s]?(.*)", re.IGNORECASE)


def _complexity_for_file(file_info: FileInfo) -> list[dict[str, object]]:
    try:
        with open(file_info.absolute_path, encoding="utf-8", errors="ignore") as f:
            source = f.read()
        blocks = cc_visit(source)
    except (OSError, SyntaxError):
        return []

    results = []
    for block in blocks:
        name = block.name if not isinstance(block, Function) or not block.classname else f"{block.classname}.{block.name}"
        results.append(
            {
                "file": file_info.path,
                "name": name,
                "complexity": block.complexity,
                "rank": cc_rank(block.complexity),
                "lineno": block.lineno,
            }
        )
    return results


def _find_todo_fixme(file_info: FileInfo) -> list[dict[str, object]]:
    try:
        with open(file_info.absolute_path, encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except OSError:
        return []

    markers = []
    for lineno, line in enumerate(lines, start=1):
        match = _TODO_PATTERN.search(line)
        if match:
            markers.append(
                {
                    "file": file_info.path,
                    "line": lineno,
                    "marker": match.group(1).upper(),
                    "text": match.group(2).strip()[:200],
                }
            )
    return markers


def analyze_complexity(python_files: list[FileInfo], all_files: list[FileInfo]) -> dict[str, object]:
    python_complexity: list[dict[str, object]] = []
    for file_info in python_files:
        python_complexity.extend(_complexity_for_file(file_info))

    todo_fixme: list[dict[str, object]] = []
    for file_info in all_files:
        if file_info.language is not None:
            todo_fixme.extend(_find_todo_fixme(file_info))

    large_files = [
        {"file": f.path, "loc": f.loc}
        for f in all_files
        if f.loc >= LARGE_FILE_LOC_THRESHOLD
    ]
    large_files.sort(key=lambda item: item["loc"], reverse=True)

    return {
        "python_function_complexity": sorted(
            python_complexity, key=lambda item: item["complexity"], reverse=True
        ),
        "todo_fixme_markers": todo_fixme,
        "large_files": large_files,
    }
