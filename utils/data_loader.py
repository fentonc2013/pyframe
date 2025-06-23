import json
import os

def load_json(filename: str):
    """
    Load a JSON file from the data directory.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", filename)
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)
