"""Rule-based validation engine for tabular clinical records."""

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


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
            error = f"{rule_id}: column {col} is null/empty"
            errors.append(error)
            logger.warning(error)
        elif kind == "between" and value is not None:
            min_v = rule.get("min")
            max_v = rule.get("max")
            if not (min_v <= value <= max_v):
                error = f"{rule_id}: column {col} outside [{min_v}, {max_v}]"
                errors.append(error)
                logger.warning(error)
        elif kind == "regex" and value is not None:
            pattern = rule.get("pattern")
            if not re.match(pattern, str(value)):
                error = f"{rule_id}: column {col} does not match pattern {pattern}"
                errors.append(error)
                logger.warning(error)
        elif kind == "unique" and value is not None:
            # Uniqueness check placeholder - requires batch context
            pass
    return errors


def validate_batch(
    records: list[dict[str, Any]],
    rules: list[dict[str, Any]],
) -> dict[str, Any]:
    invalid_rows: list[dict[str, Any]] = []
    for idx, record in enumerate(records):
        row_errors = validate_record(record, rules)
        if row_errors:
            invalid_rows.append({"row_index": idx, "errors": row_errors})

    total_records = len(records)
    invalid_count = len(invalid_rows)
    valid_count = total_records - invalid_count
    compliance_rate = round((valid_count / total_records) * 100, 2) if total_records else 0.0

    return {
        "total_records": total_records,
        "valid_records": valid_count,
        "invalid_records": invalid_count,
        "compliance_rate": compliance_rate,
        "invalid_rows": invalid_rows,
    }


def summarize_error_counts(batch_result: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in batch_result.get("invalid_rows", []):
        for error in row.get("errors", []):
            rule_id = error.split(":", 1)[0].strip() if ":" in error else "unknown_rule"
            counts[rule_id] = counts.get(rule_id, 0) + 1
    return counts
