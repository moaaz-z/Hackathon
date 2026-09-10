IGNORED_DIR_NAMES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "target",
    "vendor",
    ".idea",
    ".vscode",
    ".next",
    ".nuxt",
    "coverage",
    "htmlcov",
    ".tox",
}

IGNORED_DIR_SUFFIXES = (".egg-info",)

SKIPPED_EXTENSIONS = {
    # binaries / archives
    ".exe", ".dll", ".so", ".dylib", ".bin", ".o", ".a", ".class", ".jar",
    ".pyc", ".pyo", ".whl", ".zip", ".tar", ".gz", ".tgz", ".rar", ".7z",
    # images
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg", ".webp", ".tiff",
    # media
    ".mp3", ".mp4", ".mov", ".avi", ".wav", ".flac",
    # fonts / docs treated as binary
    ".woff", ".woff2", ".ttf", ".eot", ".pdf",
    # lockfiles (huge, not useful as "code")
    ".lock",
}

SKIPPED_FILENAMES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "uv.lock",
    "poetry.lock",
    "Cargo.lock",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".c": "C",
    ".h": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++",
    ".cs": "C#",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".md": "Markdown",
    ".sql": "SQL",
    ".sh": "Shell",
}

CONFIG_FILENAMES = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "Cargo.toml",
    "go.mod",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "Makefile",
    "tsconfig.json",
    "setup.py",
    "setup.cfg",
    ".env.example",
}

README_FILENAMES = {"README.md", "README.rst", "README.txt", "README"}

TEST_DIR_MARKERS = {"tests", "test", "__tests__", "spec"}

LARGE_FILE_LOC_THRESHOLD = 400

FRAMEWORK_EVIDENCE = {
    "FastAPI": {"fastapi"},
    "Flask": {"flask"},
    "Django": {"django"},
    "Express": {"express"},
    "NestJS": {"@nestjs/core"},
    "React": {"react"},
    "Vue": {"vue"},
    "Angular": {"@angular/core"},
    "Next.js": {"next"},
    "Spring Boot": {"spring-boot-starter", "spring-boot"},
    "Actix Web": {"actix-web"},
    "Gin": {"github.com/gin-gonic/gin"},
    "Rocket": {"rocket"},
}

ENTRY_POINT_FILENAMES = {
    "main.py", "app.py", "manage.py", "wsgi.py", "asgi.py",
    "index.js", "index.ts", "server.js", "server.ts",
    "main.go", "Program.cs", "Main.java",
}

IMPORTANT_PATH_KEYWORDS = {
    "route": 3, "router": 3, "controller": 3, "api": 2,
    "service": 3, "model": 3, "schema": 2, "handler": 2,
}
