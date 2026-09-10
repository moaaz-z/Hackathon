import ast

from hackathon.services.static_analyzer.models import (
    FileInfo,
    PythonClassInfo,
    PythonFunctionInfo,
    PythonImportInfo,
)


def _decorator_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Call):
        return _decorator_name(node.func)
    return ast.dump(node)


def _base_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ast.dump(node)


class PythonFacts:
    def __init__(self) -> None:
        self.functions: list[PythonFunctionInfo] = []
        self.classes: list[PythonClassInfo] = []
        self.imports: list[PythonImportInfo] = []
        self.parse_errors: list[str] = []


def _analyze_module(tree: ast.Module, relative_path: str, facts: PythonFacts) -> None:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            method_names = [
                item.name for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            facts.classes.append(
                PythonClassInfo(
                    file=relative_path,
                    name=node.name,
                    bases=[_base_name(base) for base in node.bases],
                    decorators=[_decorator_name(d) for d in node.decorator_list],
                    methods=method_names,
                    lineno=node.lineno,
                )
            )
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    facts.functions.append(
                        PythonFunctionInfo(
                            file=relative_path,
                            name=item.name,
                            args=[arg.arg for arg in item.args.args],
                            decorators=[_decorator_name(d) for d in item.decorator_list],
                            lineno=item.lineno,
                            is_method=True,
                            class_name=node.name,
                        )
                    )

    class_method_ids = {id(m) for c in ast.walk(tree) if isinstance(c, ast.ClassDef) for m in c.body}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and id(node) not in class_method_ids:
            facts.functions.append(
                PythonFunctionInfo(
                    file=relative_path,
                    name=node.name,
                    args=[arg.arg for arg in node.args.args],
                    decorators=[_decorator_name(d) for d in node.decorator_list],
                    lineno=node.lineno,
                    is_method=False,
                )
            )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                facts.imports.append(PythonImportInfo(file=relative_path, module=alias.name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            facts.imports.append(
                PythonImportInfo(
                    file=relative_path,
                    module=module,
                    names=[alias.name for alias in node.names],
                    is_relative=node.level > 0,
                    level=node.level,
                )
            )


def analyze_python_files(python_files: list[FileInfo]) -> PythonFacts:
    facts = PythonFacts()

    for file_info in python_files:
        try:
            with open(file_info.absolute_path, encoding="utf-8", errors="ignore") as f:
                source = f.read()
            tree = ast.parse(source, filename=file_info.path)
        except (OSError, SyntaxError, ValueError) as exc:
            facts.parse_errors.append(f"{file_info.path}: {exc}")
            continue

        _analyze_module(tree, file_info.path, facts)

    return facts
