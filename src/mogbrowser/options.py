import json
from pathlib import Path

def load_config() -> dict:
    with open("config.json", "r") as f:
        return json.load(f)

class Options:
    def __init__(self) -> None:
        data = load_config()

        self.debug: bool = data["debug"]
        self.scopes: list[dict] = data["scopes"]
        self.thumbnail_path = Path(data["thumbnail_path"])

        self.thumbnail_path.mkdir(exist_ok=True, parents=True)