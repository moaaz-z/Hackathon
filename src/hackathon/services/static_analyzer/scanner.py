import os

from hackathon.services.static_analyzer.constants import (
    CONFIG_FILENAMES,
    IGNORED_DIR_NAMES,
    IGNORED_DIR_SUFFIXES,
    LANGUAGE_BY_EXTENSION,
    README_FILENAMES,
    SKIPPED_EXTENSIONS,
    SKIPPED_FILENAMES,
)
from hackathon.services.static_analyzer.models import FileInfo


def _is_ignored_dir(name: str) -> bool:
    return (
        name in IGNORED_DIR_NAMES
        or name.endswith(IGNORED_DIR_SUFFIXES)
    )


def _read_text(
    absolute_path: str,
) -> str | None:
    try:
        with open(
            absolute_path,
            encoding="utf-8",
            errors="ignore",
        ) as f:
            return f.read()
    except OSError:
        return None


def _count_lines(
    content: str | None,
) -> int:
    if content is None or content == "":
        return 0

    return len(content.splitlines())


class ScanResult:
    def __init__(self) -> None:
        self.files: list[FileInfo] = []
        self.directory_count: int = 0
        self.readme_path: str | None = None
        self.config_files: list[str] = []


def scan_repository(
    repo_path: str,
) -> ScanResult:
    result = ScanResult()

    for root, dirnames, filenames in os.walk(repo_path):
        dirnames[:] = sorted(
            directory
            for directory in dirnames
            if not _is_ignored_dir(directory)
        )

        result.directory_count += len(dirnames)

        for filename in sorted(filenames):
            absolute_path = os.path.join(
                root,
                filename,
            )

            relative_path = os.path.relpath(
                absolute_path,
                repo_path,
            ).replace(os.sep, "/")

            if filename in SKIPPED_FILENAMES:
                continue

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension in SKIPPED_EXTENSIONS:
                continue

            if (
                filename in README_FILENAMES
                and result.readme_path is None
            ):
                result.readme_path = relative_path

            if filename in CONFIG_FILENAMES:
                result.config_files.append(
                    relative_path
                )

            try:
                size_bytes = os.path.getsize(
                    absolute_path
                )
            except OSError:
                continue

            language = LANGUAGE_BY_EXTENSION.get(
                extension
            )

            content = _read_text(
                absolute_path
            )

            loc = _count_lines(
                content
            )

            result.files.append(
                FileInfo(
                    path=relative_path,
                    absolute_path=absolute_path,
                    language=language,
                    loc=loc,
                    size_bytes=size_bytes,
                )
            )

    return result
