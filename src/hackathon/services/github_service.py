import re
import shutil
import tempfile

from git import GitCommandError, Repo

GITHUB_URL_PATTERN = re.compile(
    r"^https://github\.com/[\w.-]+/[\w.-]+?(\.git)?/?$"
)


class InvalidRepositoryUrlError(ValueError):
    pass


class RepositoryCloneError(RuntimeError):
    pass


def validate_github_url(url: str) -> str:
    url = url.strip()
    if not GITHUB_URL_PATTERN.match(url):
        raise InvalidRepositoryUrlError(
            "URL must be a public GitHub repository URL, e.g. https://github.com/owner/repo"
        )
    return url


def clone_repository(url: str) -> str:
    temp_dir = tempfile.mkdtemp(prefix="repo_")
    try:
        Repo.clone_from(url, temp_dir, depth=1)
    except GitCommandError as exc:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise RepositoryCloneError(
            "Could not clone repository. It may be private, nonexistent, or unreachable."
        ) from exc
    return temp_dir


def cleanup_repository(path: str) -> None:
    shutil.rmtree(path, ignore_errors=True)
