from hackathon.services.static_analyzer.models import FileInfo, PythonImportInfo

# Directories that commonly hold the real package root, so an import of
# "pkg.mod" should still resolve to "src/pkg/mod.py".
SOURCE_ROOT_PREFIXES = ("src", "lib", "app")


def _module_parts_for_file(file_info: FileInfo) -> list[str]:
    path_without_ext = file_info.path.rsplit(".py", 1)[0]
    parts = path_without_ext.split("/")
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return parts


def _module_name_for_file(file_info: FileInfo) -> str:
    return ".".join(_module_parts_for_file(file_info))


def _module_aliases_for_file(file_info: FileInfo) -> list[str]:
    """Dotted names a file can be imported as, most specific first."""
    parts = _module_parts_for_file(file_info)
    if not parts:
        return []

    aliases = [".".join(parts)]
    if parts[0] in SOURCE_ROOT_PREFIXES and len(parts) > 1:
        aliases.append(".".join(parts[1:]))
    return aliases


def _build_module_map(python_files: list[FileInfo]) -> dict[str, str]:
    module_to_file: dict[str, str] = {}
    for file_info in python_files:
        for alias in _module_aliases_for_file(file_info):
            # Full paths are registered first and win over stripped aliases.
            module_to_file.setdefault(alias, file_info.path)
    return module_to_file


def _resolve_absolute(module: str, importing_file: str, module_to_file: dict[str, str]) -> str | None:
    candidate = module
    while candidate:
        target = module_to_file.get(candidate)
        if target and target != importing_file:
            return target
        if "." not in candidate:
            return None
        candidate = candidate.rsplit(".", 1)[0]
    return None


def _resolve_relative(imp: PythonImportInfo, module_to_file: dict[str, str]) -> str | None:
    """Resolve `from .x import y` against the importing file's own package."""
    package_parts = imp.file.rsplit(".py", 1)[0].split("/")[:-1]

    # One dot means the current package; each extra dot climbs one level.
    climb = max(imp.level - 1, 0)
    if climb:
        if climb > len(package_parts):
            return None
        package_parts = package_parts[:-climb]

    base_parts = package_parts + (imp.module.split(".") if imp.module else [])
    if not base_parts:
        return None

    # `from . import foo` names its targets rather than the module itself.
    if not imp.module:
        for name in imp.names:
            target = module_to_file.get(".".join(base_parts + [name]))
            if target and target != imp.file:
                return target

    return _resolve_absolute(".".join(base_parts), imp.file, module_to_file)


def build_relationships(imports: list[PythonImportInfo], python_files: list[FileInfo]) -> dict[str, object]:
    module_to_file = _build_module_map(python_files)

    internal_imports: dict[str, list[str]] = {}
    for imp in imports:
        if imp.is_relative:
            resolved_file = _resolve_relative(imp, module_to_file)
        elif imp.module:
            resolved_file = _resolve_absolute(imp.module, imp.file, module_to_file)
        else:
            continue

        if resolved_file:
            internal_imports.setdefault(imp.file, [])
            if resolved_file not in internal_imports[imp.file]:
                internal_imports[imp.file].append(resolved_file)

    in_degree: dict[str, int] = {}
    for targets in internal_imports.values():
        for target in targets:
            in_degree[target] = in_degree.get(target, 0) + 1

    return {
        "internal_imports": internal_imports,
        "import_in_degree": in_degree,
    }
