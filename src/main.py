from fastapi import FastAPI, UploadFile, File
from src.validation.rules_engine import validate_batch
import json

app = FastAPI(title="Clinical Data Governance API")

@app.post("/validate")
async def validate_data(file: UploadFile = File(...)):
    content = await file.read()
    data = json.loads(content.decode())
    records = data.get("records", [])
    rules = data.get("rules", [])
    result = validate_batch(records, rules)
    return result