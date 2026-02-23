"""Compliance summary helpers."""


def compliance_summary(total_records: int, invalid_records: int) -> dict[str, float]:
    if total_records <= 0:
        return {"compliance_rate": 0.0, "invalid_records": float(invalid_records)}
    rate = ((total_records - invalid_records) / total_records) * 100
    return {"compliance_rate": round(rate, 2), "invalid_records": float(invalid_records)}
