from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

from .enums import PathType

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp",
    ".tif", ".tiff", ".svg", ".ico", ".avif", ".heic",
    ".heif", ".jxl", ".raw", ".cr2", ".cr3", ".nef",
    ".arw", ".dng", ".orf", ".rw2", ".psd",
}

VIDEO_EXTENSIONS = {
    ".mp4", ".m4v", ".mkv", ".mov", ".avi", ".wmv",
    ".flv", ".webm", ".mpeg", ".mpg", ".m4p", ".m4v",
    ".3gp", ".3g2", ".ts", ".mts", ".m2ts", ".vob",
    ".ogv", ".divx", ".xvid", ".asf", ".rm", ".rmvb",
    ".f4v", ".mpv", ".mxf", ".wtv",
}

def get_path_type(path: Path) -> PathType:
    if path.is_dir():
        return PathType.DIRECTORY

    suffix = path.suffix.lower()

    if suffix in IMAGE_EXTENSIONS:
        return PathType.IMAGE

    elif suffix in VIDEO_EXTENSIONS:
        return PathType.VIDEO

    else:
        return PathType.OTHER

def thumbnail_image(path: Path, destination: Path) -> bytes | None:
    if destination.exists():
        return destination.read_bytes()

    if not path.exists():
        return None

    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image)
        image.thumbnail((100, 100), Image.Resampling.LANCZOS)

        if image.mode not in ("RGB", "RGBA"):
            image = image.convert(
                "RGBA" if "transparency" in image.info else "RGB"
            )

        buffer = BytesIO()
        image.save(buffer, format="WEBP", quality=80, method=4)

        thumbnail = buffer.getvalue()
        destination.write_bytes(thumbnail)
        return thumbnail