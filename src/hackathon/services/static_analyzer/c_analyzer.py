import re
from typing import Any

from hackathon.services.static_analyzer.models import FileInfo


_FUNCTION_PATTERN = re.compile(
    r"""
    ^[ \t]*
    (?:
        (?:[A-Za-z_]\w*|struct\s+[A-Za-z_]\w*|enum\s+[A-Za-z_]\w*)
        [\w\s\*\[\]]*?
    )
    [ \t]+
    (?P<name>[A-Za-z_]\w*)
    \s*
    \(
        (?P<params>[^;{}]*)
    \)
    \s*
    \{
    """,
    re.MULTILINE | re.VERBOSE,
)

_INCLUDE_PATTERN = re.compile(
    r'^[ \t]*#[ \t]*include[ \t]*[<"]([^>"]+)[>"]',
    re.MULTILINE,
)

_EXCLUDED_NAMES = {
    "if",
    "for",
    "while",
    "switch",
    "return",
    "sizeof",
}


def _strip_comments(source: str) -> str:
    source = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), source, flags=re.DOTALL)
    source = re.sub(r"//[^\n]*", "", source)
    return source


def _line_number(source: str, index: int) -> int:
    return source.count("\n", 0, index) + 1


def analyze_c_files(c_files: list[FileInfo]) -> dict[str, Any]:
    functions: list[dict[str, Any]] = []
    includes: list[dict[str, Any]] = []
    parse_errors: list[str] = []
    header_files = 0

    for file_info in c_files:
        if file_info.path.lower().endswith(".h"):
            header_files += 1

        try:
            with open(file_info.absolute_path, encoding="utf-8", errors="ignore") as f:
                source = f.read()
        except OSError as exc:
            parse_errors.append(f"{file_info.path}: {exc}")
            continue

        cleaned = _strip_comments(source)

        for match in _FUNCTION_PATTERN.finditer(cleaned):
            name = match.group("name")

            if name in _EXCLUDED_NAMES:
                continue

            params = " ".join(match.group("params").split())

            functions.append(
                {
                    "file": file_info.path,
                    "name": name,
                    "params": params,
                    "lineno": _line_number(cleaned, match.start()),
                }
            )

        for match in _INCLUDE_PATTERN.finditer(cleaned):
            includes.append(
                {
                    "file": file_info.path,
                    "header": match.group(1),
                    "lineno": _line_number(cleaned, match.start()),
                }
            )

    return {
        "functions": functions,
        "includes": includes,
        "header_file_count": header_files,
        "parse_errors": parse_errors,
    }
