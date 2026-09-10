import json
import re
import tomllib
import xml.etree.ElementTree as ET
from typing import Any


def _parse_requirements_txt(content: str) -> list[dict[str, str]]:
    deps = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        match = re.match(r"^([A-Za-z0-9_.\-\[\]]+)\s*([<>=!~].*)?$", line)
        if match:
            deps.append({"name": match.group(1), "version": (match.group(2) or "").strip()})
    return deps


def _parse_pyproject_toml(content: str) -> list[dict[str, str]]:
    deps: list[dict[str, str]] = []
    try:
        data = tomllib.loads(content)
    except tomllib.TOMLDecodeError:
        return deps

    for dep in data.get("project", {}).get("dependencies", []):
        match = re.match(r"^([A-Za-z0-9_.\-\[\]]+)\s*([<>=!~].*)?$", dep)
        if match:
            deps.append({"name": match.group(1), "version": (match.group(2) or "").strip()})

    poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    for name, version in poetry_deps.items():
        if name.lower() == "python":
            continue
        deps.append({"name": name, "version": str(version)})

    return deps


def _parse_package_json(content: str) -> list[dict[str, str]]:
    deps: list[dict[str, str]] = []
    try:
        data: dict[str, Any] = json.loads(content)
    except json.JSONDecodeError:
        return deps

    for section in ("dependencies", "devDependencies"):
        for name, version in data.get(section, {}).items():
            deps.append({"name": name, "version": str(version)})
    return deps


def _parse_pom_xml(content: str) -> list[dict[str, str]]:
    deps: list[dict[str, str]] = []
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        return deps

    namespace_match = re.match(r"\{(.*)\}", root.tag)
    ns = {"m": namespace_match.group(1)} if namespace_match else {}
    tag = lambda name: f"m:{name}" if ns else name  # noqa: E731

    for dependency in root.findall(f".//{tag('dependency')}", ns):
        group_id = dependency.findtext(tag("groupId"), default="", namespaces=ns)
        artifact_id = dependency.findtext(tag("artifactId"), default="", namespaces=ns)
        version = dependency.findtext(tag("version"), default="", namespaces=ns)
        name = f"{group_id}:{artifact_id}" if group_id else artifact_id
        if artifact_id:
            deps.append({"name": name, "version": version or ""})

    return deps


def _parse_cargo_toml(content: str) -> list[dict[str, str]]:
    deps: list[dict[str, str]] = []
    try:
        data = tomllib.loads(content)
    except tomllib.TOMLDecodeError:
        return deps

    for name, spec in data.get("dependencies", {}).items():
        if isinstance(spec, dict):
            version = str(spec.get("version", ""))
        else:
            version = str(spec)
        deps.append({"name": name, "version": version})
    return deps


def _parse_go_mod(content: str) -> list[dict[str, str]]:
    deps: list[dict[str, str]] = []
    in_require_block = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("require ("):
            in_require_block = True
            continue
        if in_require_block and stripped == ")":
            in_require_block = False
            continue

        if in_require_block:
            parts = stripped.split()
        elif stripped.startswith("require "):
            parts = stripped.removeprefix("require ").split()
        else:
            continue

        if len(parts) >= 2:
            deps.append({"name": parts[0], "version": parts[1]})

    return deps


_PARSERS = {
    "requirements.txt": ("python", _parse_requirements_txt),
    "pyproject.toml": ("python", _parse_pyproject_toml),
    "package.json": ("node", _parse_package_json),
    "pom.xml": ("java", _parse_pom_xml),
    "Cargo.toml": ("rust", _parse_cargo_toml),
    "go.mod": ("go", _parse_go_mod),
}


def collect_dependencies(repo_path: str, config_file_paths: list[str]) -> dict[str, list[dict[str, str]]]:
    dependencies: dict[str, list[dict[str, str]]] = {}

    for relative_path in config_file_paths:
        filename = relative_path.rsplit("/", 1)[-1]
        parser_entry = _PARSERS.get(filename)
        if not parser_entry:
            continue

        ecosystem, parser = parser_entry
        try:
            with open(f"{repo_path}/{relative_path}", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except OSError:
            continue

        parsed = parser(content)
        if parsed:
            dependencies.setdefault(ecosystem, []).extend(parsed)

    return dependencies
