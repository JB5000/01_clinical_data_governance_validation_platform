from fastapi import FastAPI, UploadFile, File, Request
from src.validation.rules_engine import validate_batch
import json
import yaml
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Clinical Data Governance API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

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