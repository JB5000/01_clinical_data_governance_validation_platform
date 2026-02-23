from src.reporting.compliance import compliance_summary
from src.validation.rules_engine import validate_record


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
