import argparse
import json
import yaml
from src.validation.rules_engine import validate_batch

def main():
    parser = argparse.ArgumentParser(description="Validate clinical data")
    parser.add_argument("data_file", help="JSON file with records")
    parser.add_argument("--config", default="configs/config.yaml", help="YAML config file")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)
    rules = config["validation"]["default_rules"]

    with open(args.data_file) as f:
        data = json.load(f)
    records = data["records"]

    result = validate_batch(records, rules)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()