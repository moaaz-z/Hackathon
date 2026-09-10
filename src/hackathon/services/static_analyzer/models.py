from dataclasses import dataclass, field


@dataclass
class FileInfo:
    path: str  # relative to repo root, forward slashes
    absolute_path: str
    language: str | None
    loc: int
    size_bytes: int


@dataclass
class PythonFunctionInfo:
    file: str
    name: str
    args: list[str]
    decorators: list[str]
    lineno: int
    is_method: bool
    class_name: str | None = None


@dataclass
class PythonClassInfo:
    file: str
    name: str
    bases: list[str]
    decorators: list[str]
    methods: list[str]
    lineno: int


@dataclass
class PythonImportInfo:
    file: str
    module: str
    names: list[str] = field(default_factory=list)
    is_relative: bool = False
    level: int = 0  # number of leading dots on a relative import
