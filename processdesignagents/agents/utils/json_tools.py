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


def convert_streams_json_to_markdown(streams_json: str) -> str:
    """Render stream summary JSON into a transposed Markdown table."""
    sanitized_json, payload = extract_first_json_document(streams_json)
    if payload is None:
        return sanitized_json

    data = payload if isinstance(payload, dict) else {"streams": payload}
    streams = data.get("streams")
    if not isinstance(streams, list) or not streams:
        return sanitized_json

    metadata = data.get("metadata", {}) or {}
    property_order = _normalize_property_order(metadata.get("property_order"), streams)
    component_order = _normalize_component_order(metadata.get("component_order"), streams)
    component_basis = metadata.get("component_basis")
    global_notes = metadata.get("assumptions") or data.get("assumptions")

    headers = ["Attribute"] + [str(stream.get("id") or f"S{index}") for index, stream in enumerate(streams, start=1)]
    lines: list[str] = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]

    def row(label: str, values: list[str]) -> None:
        row_values = [label] + [value if value is not None else "" for value in values]
        lines.append("| " + " | ".join(row_values) + " |")

    row("Name / Description", [_stringify(stream.get("name") or stream.get("description")) for stream in streams])
    descriptions = [_stringify(stream.get("description")) for stream in streams]
    if any(descriptions):
        row("Detailed Description", descriptions)

    row("From", [_stringify(stream.get("from")) for stream in streams])
    row("To", [_stringify(stream.get("to")) for stream in streams])
    row("Phase", [_stringify(stream.get("phase")) for stream in streams])

    for prop_key, prop_label, prop_units in property_order:
        label = prop_label or prop_key
        if prop_units:
            label = f"{label} [{prop_units}]"
        row(label, [_extract_property_value(stream, prop_key) for stream in streams])

    if component_order:
        basis_label = f"**({component_basis})**" if component_basis else ""
        row("**Key Components**", [basis_label for _ in streams])
        for component_name in component_order:
            row(component_name, [
                _stringify(_get_component_value(stream, component_name))
                for stream in streams
            ])

    row("Notes", [_stringify(stream.get("notes")) for stream in streams])

    markdown_table = "\n".join(lines)

    notes_lines: list[str] = []
    if isinstance(global_notes, list) and global_notes:
        notes_lines.append("## Notes")
        for note in global_notes:
            notes_lines.append(f"- {_stringify(note)}")
    elif isinstance(global_notes, str) and global_notes.strip():
        notes_lines.append("## Notes")
        for note_line in global_notes.strip().splitlines():
            notes_lines.append(f"- {note_line.strip()}")

    if notes_lines:
        markdown_table = markdown_table + "\n\n" + "\n".join(notes_lines)

    return markdown_table or sanitized_json


def convert_equipment_json_to_markdown(equipment_json: str) -> str:
    """Render equipment summary JSON into grouped Markdown tables."""
    sanitized_json, payload = extract_first_json_document(equipment_json)
    if payload is None:
        return sanitized_json

    metadata: dict = {}
    equipment_list = None
    if isinstance(payload, dict):
        metadata = payload.get("metadata") or {}
        equipment_list = payload.get("equipment")
    elif isinstance(payload, list):
        equipment_list = payload
    else:
        return sanitized_json

    if not isinstance(equipment_list, list) or not equipment_list:
        return sanitized_json

    groups = metadata.get("groups")
    assumptions = metadata.get("assumptions")

    lines: list[str] = []
    used_ids: set[str] = set()

    def render_group(title: str, members: list[dict]) -> None:
        if not members:
            return
        lines.append(f"### {title}")
        headers = [
            "Equipment ID",
            "Name",
            "Service",
            "Type",
            "Streams In",
            "Streams Out",
            "Duty / Load",
            "Key Parameters",
            "Notes",
        ]
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join("---" for _ in headers) + " |")

        for item in members:
            if not isinstance(item, dict):
                continue
            equipment_id = _stringify(item.get("id"))
            if equipment_id:
                used_ids.add(equipment_id)
            streams_in = item.get("streams_in") or item.get("streamsIn")
            streams_out = item.get("streams_out") or item.get("streamsOut")
            key_params = item.get("key_parameters") or item.get("keyParameters")

            row = [
                equipment_id,
                _stringify(item.get("name")),
                _stringify(item.get("service")),
                _stringify(item.get("type")),
                _format_sequence(streams_in),
                _format_sequence(streams_out),
                _stringify(item.get("duty_or_load") or item.get("duty") or item.get("load")),
                _format_sequence(key_params),
                _stringify(item.get("notes")),
            ]
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")  # Blank line between groups

    if isinstance(groups, list) and groups:
        for group in groups:
            if not isinstance(group, dict):
                continue
            group_name = _stringify(group.get("name") or group.get("title") or "Equipment")
            member_ids = group.get("ids") or group.get("equipment_ids") or group.get("members")
            members: list[dict] = []
            if isinstance(member_ids, list):
                members = [
                    item for item in equipment_list
                    if isinstance(item, dict) and item.get("id") in member_ids
                ]
            else:
                members = [
                    item for item in equipment_list
                    if isinstance(item, dict) and _stringify(item.get("group")).lower() == group_name.lower()
                ]
            render_group(group_name or "Equipment", members)

    # Render ungrouped equipment
    ungrouped = [
        item for item in equipment_list
        if isinstance(item, dict) and _stringify(item.get("id")) not in used_ids
    ]
    if groups and ungrouped:
        render_group("Other Equipment", ungrouped)
    elif not groups:
        render_group("Equipment Summary", equipment_list)

    if isinstance(assumptions, list) and assumptions:
        lines.append("## Notes")
        for assumption in assumptions:
            lines.append(f"- {_stringify(assumption)}")
    elif isinstance(assumptions, str) and assumptions.strip():
        lines.append("## Notes")
        for note_line in assumptions.strip().splitlines():
            lines.append(f"- {note_line.strip()}")

    markdown = "\n".join(lines).strip()
    return markdown or sanitized_json


def convert_risk_json_to_markdown(risk_json: str) -> str:
    """Render safety risk JSON into Markdown hazard sections."""
    sanitized_json, payload = extract_first_json_document(risk_json)
    if payload is None:
        return sanitized_json

    hazards = None
    overall = None
    if isinstance(payload, dict):
        hazards = payload.get("hazards")
        overall = payload.get("overall_assessment")
    elif isinstance(payload, list):
        hazards = payload

    if not isinstance(hazards, list) or not hazards:
        return sanitized_json

    lines: list[str] = []
    for idx, hazard in enumerate(hazards, start=1):
        if not isinstance(hazard, dict):
            continue
        title = _stringify(hazard.get("title") or hazard.get("name") or f"Hazard {idx}")
        severity = _stringify(hazard.get("severity"))
        likelihood = _stringify(hazard.get("likelihood"))
        risk_score = _stringify(hazard.get("risk_score") or hazard.get("riskScore"))
        lines.append(f"## Hazard {idx}: {title}")
        if severity or likelihood or risk_score:
            lines.append(f"**Severity:** {severity or 'TBD'}")
            lines.append(f"**Likelihood:** {likelihood or 'TBD'}")
            lines.append(f"**Risk Score:** {risk_score or 'TBD'}")
            lines.append("")

        def render_list(header: str, values):
            if isinstance(values, (list, tuple)) and values:
                lines.append(f"### {header}")
                for value in values:
                    value_str = _stringify(value)
                    if value_str:
                        lines.append(f"- {value_str}")
                lines.append("")

        render_list("Causes", hazard.get("causes"))
        render_list("Consequences", hazard.get("consequences"))
        render_list("Mitigations", hazard.get("mitigations"))
        notes = hazard.get("notes") or hazard.get("observations")
        render_list("Notes", notes)

    if isinstance(overall, dict) and overall:
        lines.append("## Overall Assessment")
        risk_level = _stringify(overall.get("risk_level") or overall.get("overall_risk_level"))
        compliance = overall.get("compliance_notes") or overall.get("notes")
        if risk_level:
            lines.append(f"- Overall Risk Level: {risk_level}")
        if isinstance(compliance, (list, tuple)):
            for note in compliance:
                note_str = _stringify(note)
                if note_str:
                    lines.append(f"- {note_str}")
        elif isinstance(compliance, str) and compliance.strip():
            lines.append(f"- {compliance.strip()}")

    markdown = "\n".join(line for line in lines if line is not None).strip()
    return markdown or sanitized_json


def _normalize_property_order(property_order, streams):
    normalized: list[tuple[str, str | None, str | None]] = []
    if isinstance(property_order, list):
        for entry in property_order:
            if isinstance(entry, dict):
                key = entry.get("key") or entry.get("name")
                if not key:
                    continue
                label = entry.get("label") or key
                units = entry.get("units")
                normalized.append((str(key), str(label) if label else None, str(units) if units else None))
            elif isinstance(entry, str):
                normalized.append((entry, entry, None))
    if not normalized:
        first_stream = next((stream for stream in streams if isinstance(stream, dict)), {})
        properties = first_stream.get("properties", {})
        if isinstance(properties, dict):
            for key in properties.keys():
                normalized.append((str(key), str(key).replace("_", " ").title(), None))
    return normalized


def _normalize_component_order(component_order, streams):
    ordered: list[str] = []
    if isinstance(component_order, list):
        for component in component_order:
            if isinstance(component, str):
                ordered.append(component)
            elif isinstance(component, dict) and "name" in component:
                ordered.append(str(component["name"]))
    if not ordered:
        seen: set[str] = set()
        for stream in streams:
            components = stream.get("components")
            if isinstance(components, dict):
                for name in components.keys():
                    if name not in seen:
                        seen.add(name)
                        ordered.append(str(name))
            elif isinstance(components, list):
                for component in components:
                    if isinstance(component, dict):
                        name = component.get("name")
                        if name and name not in seen:
                            seen.add(name)
                            ordered.append(str(name))
    return ordered


def _extract_property_value(stream, prop_key: str) -> str:
    properties = stream.get("properties")
    if isinstance(properties, dict):
        value = properties.get(prop_key)
    elif isinstance(properties, list):
        matching = next(
            (prop for prop in properties if isinstance(prop, dict) and prop.get("key") == prop_key or prop.get("name") == prop_key),
            None,
        )
        value = matching.get("value") if isinstance(matching, dict) else matching
    else:
        value = None
    if isinstance(value, dict):
        val_text = value.get("value")
        units = value.get("units")
        if val_text is None:
            return ""
        if units and units not in str(val_text):
            return f"{val_text} {units}"
        return str(val_text)
    return _stringify(value)


def _get_component_value(stream, component_name: str):
    components = stream.get("components")
    if isinstance(components, dict):
        return components.get(component_name)
    if isinstance(components, list):
        for component in components:
            if isinstance(component, dict):
                name = component.get("name")
                if name == component_name:
                    return component.get("value")
    return ""


def _stringify(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return f"{value}"
    return str(value)


def _format_sequence(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        items = [_stringify(item) for item in value if item is not None]
        return ", ".join(item for item in items if item)
    return _stringify(value)
