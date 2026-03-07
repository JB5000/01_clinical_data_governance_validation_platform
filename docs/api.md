# API Documentation

## Endpoint: POST /validate

Upload a JSON file with records and rules for validation.

### Request
- Content-Type: multipart/form-data
- File: JSON with structure:
```json
{
  "records": [
    {"patient_id": "P001", "age": 34}
  ],
  "rules": [
    {"id": "age_range", "type": "between", "column": "age", "min": 0, "max": 120}
  ]
}
```

### Response
```json
{
  "total_records": 1,
  "valid_records": 1,
  "invalid_records": 0,
  "compliance_rate": 100.0,
  "invalid_rows": []
}
```