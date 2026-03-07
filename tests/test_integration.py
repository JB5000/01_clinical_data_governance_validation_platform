import pytest
import yaml
from src.validation.rules_engine import validate_batch

def test_validate_batch_with_config():
    with open("configs/config.yaml") as f:
        config = yaml.safe_load(f)
    rules = config["validation"]["default_rules"]
    records = [
        {"patient_id": "P001", "age": 34, "email": "test@example.com"},
        {"patient_id": "", "age": 21, "email": "invalid"},
    ]
    result = validate_batch(records, rules)
    assert result["invalid_records"] == 1