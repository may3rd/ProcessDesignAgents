from __future__ import annotations

import json
import re

_INVALID_ESCAPE_PATTERN = re.compile(r"(?<!\\)\\([^\"\\/bfnrtu])")
_CONTROL_ESCAPE_PATTERN = re.compile(r"(?<!\\)\\([btnfrBTNFR])(?=[A-Za-z])")


def extract_first_json_document(raw_text: str) -> tuple[str, object | None]:
    """Strip fences and isolate the first JSON document from a mixed payload."""
    cleaned = raw_text.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 2 and lines[-1].strip() == "```":
            cleaned = "\n".join(lines[1:-1]).strip()

    normalized = _escape_problematic_json_sequences(cleaned)
    decoder = json.JSONDecoder()
    start_index = 0

    while start_index < len(normalized):
        ch = normalized[start_index]
        if ch.isspace():
            start_index += 1
            continue
        if ch not in "{[":
            start_index += 1
            continue
        try:
            payload, end_index = decoder.raw_decode(normalized, start_index)
            sanitized_payload = _sanitize_json_payload(payload)
            sanitized = json.dumps(sanitized_payload, ensure_ascii=False)
            return sanitized, sanitized_payload
        except json.JSONDecodeError:
            start_index += 1

    return normalized, None


def _sanitize_json_payload(node):
    if isinstance(node, dict):
        return {key: _sanitize_json_payload(value) for key, value in node.items()}
    if isinstance(node, list):
        return [_sanitize_json_payload(item) for item in node]
    if isinstance(node, str):
        return _sanitize_string_value(node)
    return node


def _sanitize_string_value(value: str) -> str:
    if "\t" in value:
        value = value.replace("\t", "\\t")
    return value


def _escape_problematic_json_sequences(text: str) -> str:
    text = _CONTROL_ESCAPE_PATTERN.sub(lambda match: "\\\\" + match.group(1), text)
    text = _INVALID_ESCAPE_PATTERN.sub(lambda match: "\\\\" + match.group(1), text)
    return text


def convert_evaluations_json_to_markdown(evaluations_json: str) -> str:
    """Convert structured evaluation JSON into a readable Markdown summary."""
    sanitized_json, payload = extract_first_json_document(evaluations_json)
    if payload is None:
        return sanitized_json

    evaluations = None
    if isinstance(payload, dict):
        evaluations = payload.get("evaluations")
    elif isinstance(payload, list):
        evaluations = payload

    if not isinstance(evaluations, list):
        return sanitized_json

    lines: list[str] = []
    concept_counter = 0

    for evaluation in evaluations:
        if not isinstance(evaluation, dict):
            continue

        concept_counter += 1
        name = evaluation.get("name", "Untitled Concept")
        maturity = evaluation.get("maturity")
        summary = evaluation.get("summary")
        feasibility = evaluation.get("feasibility_score")
        risks = evaluation.get("risks") or {}
        recommendations = evaluation.get("recommendations") or []
        concept_info = evaluation.get("concept") or {}

        lines.append("---")
        lines.append(f"## Concept {concept_counter}. {name}")
        if isinstance(maturity, str) and maturity:
            lines.append(f"**Maturity:** {maturity.replace('_', ' ').title()}")
        if isinstance(feasibility, int):
            lines.append(f"**Feasibility Score:** {feasibility}")
        if isinstance(summary, str) and summary:
            lines.append(f"**Summary:** {summary}")

        if isinstance(risks, dict) and risks:
            lines.append("**Risks:**")
            for risk_key, risk_text in risks.items():
                if not isinstance(risk_text, str) or not risk_text.strip():
                    continue
                label = risk_key.replace("_", " ").title()
                lines.append(f"- {label}: {risk_text}")

        if isinstance(recommendations, list) and recommendations:
            lines.append("**Recommendations:**")
            for rec in recommendations:
                lines.append(f"- {rec}")

        if isinstance(concept_info, dict) and concept_info:
            description = concept_info.get("description")
            unit_operations = concept_info.get("unit_operations") or []
            key_benefits = concept_info.get("key_benefits") or []

            if isinstance(description, str) and description:
                lines.append(f"**Concept Description:** {description}")

            if isinstance(unit_operations, list) and unit_operations:
                lines.append("**Concept Unit Operations:**")
                for unit in unit_operations:
                    lines.append(f"- {unit}")

            if isinstance(key_benefits, list) and key_benefits:
                lines.append("**Concept Key Benefits:**")
                for benefit in key_benefits:
                    lines.append(f"- {benefit}")

    if not lines:
        return sanitized_json

    return "\n".join(lines)
