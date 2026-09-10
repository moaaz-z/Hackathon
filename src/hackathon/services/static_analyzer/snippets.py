MAX_SNIPPET_LINES = 40
MAX_SNIPPET_CHARS = 1500


def extract_snippets(repo_path: str, important_files: list[dict[str, object]]) -> dict[str, str]:
    snippets: dict[str, str] = {}

    for entry in important_files:
        relative_path = entry["path"]  # type: ignore[index]
        try:
            with open(f"{repo_path}/{relative_path}", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()[:MAX_SNIPPET_LINES]
        except OSError:
            continue

        snippet = "".join(lines)[:MAX_SNIPPET_CHARS]
        snippets[relative_path] = snippet

    return snippets
