from datetime import datetime
import logging
import sqlite3
from io import BytesIO
from pathlib import Path
from uuid import NAMESPACE_DNS, uuid3, UUID
from concurrent.futures import ThreadPoolExecutor, as_completed

from PIL import Image, ImageOps

from .util import get_path_type
from .enums import PathType


class Data:
    BATCH_INTERVAL = 5

    def __init__(self):
        self.logger = logging.getLogger("data")
        self.connection = sqlite3.connect(
            "mogbrowser.db",
            check_same_thread=False
        )
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode = WAL;")
        self.connection.execute("PRAGMA busy_timeout = 5000;")
        self.connection.execute("PRAGMA foreign_keys = 1;")

        script = """
            CREATE TABLE IF NOT EXISTS paths (
                id TEXT PRIMARY KEY,
                path TEXT NOT NULL UNIQUE,
                added REAL NOT NULL
            );
        """

        self.connection.executescript(script)
        self.connection.commit()

        self.paths: dict[Path, UUID] = {}
        self.load_cache()

    def load_cache(self):
        cursor = self.connection.execute("SELECT * FROM paths")
        rows = cursor.fetchall()

        for row in rows:
            self.paths[Path(row["path"])] = UUID(row["id"])

    def close(self):
        self.connection.close()

    def add_paths_and_thumbnail(self, paths: list[Path]):
        def create_thumbnail(image_path: Path) -> bytes:
            with Image.open(image_path) as image:
                image = ImageOps.exif_transpose(image)
                image.thumbnail((320, 240), Image.Resampling.LANCZOS)

                if image.mode not in ("RGB", "RGBA"):
                    image = image.convert(
                        "RGBA" if "transparency" in image.info else "RGB"
                    )

                buffer = BytesIO()
                image.save(buffer, format="WEBP", quality=80, method=4)
                return buffer.getvalue()

        if not paths:
            return

        non_unassimilable = {
            path
            for path in paths
            if get_path_type(path) != PathType.IMAGE
        }

        for non_thumbnail in non_unassimilable:
            self.add_path(non_thumbnail)

        images = {
            path
            for path in paths
            if get_path_type(path) == PathType.IMAGE
        }

        total = len(images)
        thumbnailed = 0
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(create_thumbnail, image): image
                for image in images
            }

            for future in as_completed(futures):
                path = futures[future]

                try:
                    thumbnail = future.result()

                    path_id = self.add_path(path)
                    Path(f"thumbnails/{path_id}.webp").write_bytes(thumbnail)

                except Exception as e:
                    self.logger.exception(f"Failed to thumbnail image ({path}): {e}")
                    continue

                thumbnailed += 1
                self.logger.info(f"[THUMBNAIL] {thumbnailed}/{total} {path}")

    def add_path(self, path: Path) -> UUID:
        path_id = uuid3(NAMESPACE_DNS, str(path))
        query = """
            INSERT INTO paths (id, path, added) VALUES (?, ?, ?)
        """

        try:
            with self.connection:
                self.connection.execute(query, (str(path_id), str(path), datetime.now().timestamp()))

            self.paths[path] = path_id

        except sqlite3.IntegrityError:
            pass

        return path_id