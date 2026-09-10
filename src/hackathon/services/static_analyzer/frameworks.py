from hackathon.services.static_analyzer.constants import FRAMEWORK_EVIDENCE


def detect_frameworks(dependencies: dict[str, list[dict[str, str]]]) -> list[dict[str, object]]:
    all_dependency_names = {
        dep["name"].lower()
        for deps in dependencies.values()
        for dep in deps
    }

    detected = []
    for framework, indicators in FRAMEWORK_EVIDENCE.items():
        matched = {indicator for indicator in indicators if indicator.lower() in all_dependency_names}
        if matched:
            detected.append({"name": framework, "evidence": sorted(matched)})

    return detected
