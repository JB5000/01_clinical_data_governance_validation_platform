from fastapi import FastAPI, UploadFile, File
from src.validation.rules_engine import validate_batch
import json
import yaml

app = FastAPI(title="Clinical Data Governance API")

@app.on_event("startup")
def load_config():
    global default_rules
    with open("configs/config.yaml") as f:
        config = yaml.safe_load(f)
    default_rules = config["validation"]["default_rules"]

@app.post("/validate")
async def validate_data(file: UploadFile = File(...)):
    content = await file.read()
    data = json.loads(content.decode())
    records = data.get("records", [])
    rules = data.get("rules", default_rules)
    result = validate_batch(records, rules)
    return result

@app.get("/rules")
def get_default_rules():
    return {"rules": default_rules}