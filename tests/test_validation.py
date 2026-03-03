from src.reporting.compliance import compliance_summary
from src.validation.rules_engine import summarize_error_counts, validate_batch, validate_record


def test_validate_record_reports_null_and_out_of_range() -> None:
    rules = [
        {"id": "patient_id_required", "type": "not_null", "column": "patient_id"},
        {"id": "age_range", "type": "between", "column": "age", "min": 0, "max": 120},
    ]
    rec = {"patient_id": "", "age": 140}
    errs = validate_record(rec, rules)
    assert len(errs) == 2


def test_compliance_summary_rate() -> None:
    summary = compliance_summary(total_records=100, invalid_records=7)
    assert summary["compliance_rate"] == 93.0


def test_validate_batch_summarizes_invalid_rows() -> None:
    rules = [
        {"id": "patient_id_required", "type": "not_null", "column": "patient_id"},
        {"id": "age_range", "type": "between", "column": "age", "min": 0, "max": 120},
    ]
    records = [
        {"patient_id": "P001", "age": 34},
        {"patient_id": "", "age": 21},
        {"patient_id": "P003", "age": 999},
    ]

    result = validate_batch(records, rules)
    assert result["total_records"] == 3
    assert result["invalid_records"] == 2
    assert result["valid_records"] == 1
    assert result["compliance_rate"] == 33.33
    assert [row["row_index"] for row in result["invalid_rows"]] == [1, 2]


def test_summarize_error_counts_by_rule() -> None:
    rules = [
        {"id": "patient_id_required", "type": "not_null", "column": "patient_id"},
        {"id": "age_range", "type": "between", "column": "age", "min": 0, "max": 120},
    ]
    records = [
        {"patient_id": "", "age": 300},
        {"patient_id": "", "age": 20},
    ]

    result = validate_batch(records, rules)
    counts = summarize_error_counts(result)
    assert counts["patient_id_required"] == 2
    assert counts["age_range"] == 1
