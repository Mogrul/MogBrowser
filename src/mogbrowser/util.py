from pathlib import Path

from .enums import PathType

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

def get_path_type(path: Path) -> PathType:
    suffix = path.suffix.lower()

    if suffix in VIDEO_EXTENSIONS:
        return PathType.VIDEO

    elif suffix in IMAGE_EXTENSIONS:
        return PathType.IMAGE

    else:
        if path.is_dir():
            return PathType.DIRECTORY

        else:
            return PathType.OTHER