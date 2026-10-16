import json
import sys
from argparse import Namespace, ArgumentParser
from pathlib import Path


DEFAULT_JSON = {
    "scopes": {
        "root": {
            "path": "./"
        }
    }
}

def get_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging."
    )

    parser.add_argument(
        "--thumbnail-path",
        default="data/thumbnails",
        type=Path,
        help="Set the path where thumbnails are stored, changing this would mean the media need to be thumbnail again."
    )

    parser.add_argument(
        "--ffmpeg-path",
        default="",
        type=Path,
        help="Set a path to FFmpeg.exe or linux equivalent for video thumbnails."
    )

    parser.add_argument(
        "--ffprobe-path",
        default="",
        type=Path,
        help="Set a path to FFprobe.exe or linux equivalent for video thumbnails."
    )

    parser.add_argument(
        "--config-path",
        default="data/config.json",
        type=Path,
        help="Path to config.json file."
    )

    return parser.parse_args()

def load_json(path: Path) -> dict:
    with path.open("r") as f:
        return json.load(f)

def generate_config(path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(DEFAULT_JSON, f, indent=4)

class Config:
    def __init__(self):
        args = get_args()

        self.debug: bool = args.debug

        self.thumbnail_path: Path = args.thumbnail_path
        self.ffmpeg_path: Path = args.ffmpeg_path
        self.ffprobe_path: Path = args.ffprobe_path
        self.config_path: Path = args.config_path

        if not self.config_path.exists():
            print(f"{self.config_path} doesn't exist, generating one and closing.")
            generate_config(self.config_path)
            sys.exit()

        json_data = load_json(self.config_path)

        self.scopes: dict[str, dict[str, str]] = json_data["scopes"]

        self.verify()

    def verify(self):
        success = True

        self.thumbnail_path.mkdir(parents=True, exist_ok=True)

        if not self.scopes:
            print(f"No scopes in config.json, cannot display anything.")
            success = False

        if not success:
            sys.exit()


config = Config()