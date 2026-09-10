from hackathon.services.static_analyzer.constants import TEST_DIR_MARKERS
from hackathon.services.static_analyzer.models import FileInfo


def _is_test_file(path: str) -> bool:
    lowered = path.lower()
    filename = lowered.rsplit("/", 1)[-1]
    path_parts = lowered.split("/")[:-1]

    if any(part in TEST_DIR_MARKERS for part in path_parts):
        return True
    if filename.startswith("test_") or filename.endswith("_test.py"):
        return True
    if filename.endswith((".test.js", ".test.ts", ".spec.js", ".spec.ts", ".test.tsx", ".spec.tsx")):
        return True
    return False


def detect_tests(files: list[FileInfo]) -> dict[str, object]:
    code_files = [f for f in files if f.language is not None]
    test_files = [f.path for f in code_files if _is_test_file(f.path)]

    total_code_files = len(code_files)
    ratio = round(len(test_files) / total_code_files, 4) if total_code_files else 0.0

    return {
        "test_files": test_files,
        "test_file_count": len(test_files),
        "total_code_files": total_code_files,
        "test_file_ratio": ratio,
        "note": (
            "test_file_ratio is based on test file counts only. "
            "No test execution or coverage instrumentation was performed."
        ),
    }
