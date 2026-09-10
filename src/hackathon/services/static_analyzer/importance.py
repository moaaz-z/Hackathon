from hackathon.services.static_analyzer.constants import (
    ENTRY_POINT_FILENAMES,
    IMPORTANT_PATH_KEYWORDS,
    README_FILENAMES,
)
from hackathon.services.static_analyzer.models import FileInfo

MIN_IMPORTANT_FILES = 10
MAX_IMPORTANT_FILES = 20

ENTRY_POINT_SCORE = 5
README_SCORE = 4
MAX_IN_DEGREE_SCORE = 5
MAX_COMPLEXITY_SCORE = 5
MAX_LOC_BONUS = 2


def select_important_files(
    files: list[FileInfo],
    relationships: dict[str, object],
    complexity: dict[str, object],
) -> list[dict[str, object]]:
    in_degree: dict[str, int] = relationships.get("import_in_degree", {})  # type: ignore[assignment]

    complexity_by_file: dict[str, int] = {}
    for entry in complexity.get("python_function_complexity", []):  # type: ignore[union-attr]
        complexity_by_file[entry["file"]] = complexity_by_file.get(entry["file"], 0) + entry["complexity"]

    scored = []
    for file_info in files:
        filename = file_info.path.rsplit("/", 1)[-1]
        is_readme = filename in README_FILENAMES

        # READMEs are the primary evidence for project purpose, so they are
        # kept even when the extension maps to no known language.
        if file_info.language is None and not is_readme:
            continue

        score = 0.0
        reasons = []

        if filename in ENTRY_POINT_FILENAMES:
            score += ENTRY_POINT_SCORE
            reasons.append("entry point")

        if is_readme:
            score += README_SCORE
            reasons.append("project README")

        lowered_path = file_info.path.lower()
        for keyword, weight in IMPORTANT_PATH_KEYWORDS.items():
            if keyword in lowered_path:
                score += weight
                reasons.append(f"path contains '{keyword}'")
                break

        incoming = in_degree.get(file_info.path, 0)
        if incoming:
            score += min(incoming, MAX_IN_DEGREE_SCORE)
            reasons.append(f"imported by {incoming} internal file(s)")

        file_complexity = complexity_by_file.get(file_info.path, 0)
        if file_complexity:
            score += min(file_complexity / 5, MAX_COMPLEXITY_SCORE)
            reasons.append(f"cyclomatic complexity total {file_complexity}")

        # Size alone does not make a file important. LOC is only a tie-breaker
        # bonus for files that already matched a substantive signal, so nothing
        # is ever reported as important without a stated reason.
        if not reasons:
            continue

        if file_info.loc:
            score += min(file_info.loc / 200, MAX_LOC_BONUS)

        scored.append({"path": file_info.path, "score": round(score, 2), "reasons": reasons})

    scored.sort(key=lambda item: item["score"], reverse=True)

    if len(scored) <= MIN_IMPORTANT_FILES:
        return scored
    return scored[:MAX_IMPORTANT_FILES]
