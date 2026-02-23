"""Rule-based validation engine for tabular clinical records."""

from typing import Any


def _is_empty(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def validate_record(record: dict[str, Any], rules: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for rule in rules:
        rule_id = rule.get("id", "unknown_rule")
        kind = rule.get("type")
        col = rule.get("column")
        value = record.get(col)

        if kind == "not_null" and _is_empty(value):
            errors.append(f"{rule_id}: column {col} is null/empty")
        elif kind == "between" and value is not None:
            min_v = rule.get("min")
            max_v = rule.get("max")
            if not (min_v <= value <= max_v):
                errors.append(f"{rule_id}: column {col} outside [{min_v}, {max_v}]")
    return errors
