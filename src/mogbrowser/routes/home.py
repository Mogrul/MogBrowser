import logging
from math import ceil
from pathlib import Path

from flask import Blueprint, render_template, request, abort, current_app

from mogbrowser import scopes, data, thumbnail_path
from mogbrowser.util import get_path_type

home = Blueprint("home", __name__)

@home.route("/")
def index():
    logger: logging.Logger = current_app.logger
    scope = request.args.get("scope", "root")
    path = request.args.get("path", "")
    page = request.args.get("page", 1, type=int)

    if scope not in scopes:
        logger.error(f"Scope {scope} not in scopes: {scopes}")
        return abort(404)

    path = Path(path)

    if not path.exists() or not path.is_dir():
        logger.error(f"Path doesn't exist: {path}")
        return abort(404)

    inner_paths = sorted(path.iterdir(), reverse=True)

    per_page = 50
    total_items = len(inner_paths)
    total_pages = ceil(total_items / per_page)
    page = max(1, min(page, total_pages or 1))

    start = (page - 1) * per_page
    paginated_paths = inner_paths[start:start + per_page]

    data.add_paths_and_thumbnail(paginated_paths)

    sorted_paths = []
    for paginated_path in paginated_paths:
        path_type = get_path_type(paginated_path)
        path_id = data.paths.get(paginated_path)

        path_data = {
            "path": paginated_path,
            "type": path_type,
            "id": path_id,
        }

        if path_id and (thumbnail_path / (str(path_id) + ".webp")).is_file():
            path_data["thumbnail"] = thumbnail_path / str(path_id)

        sorted_paths.append(path_data)

    return render_template(
        "gallery.html",
        paths=sorted_paths,
        page=page,
        total_pages=total_pages,
        total_items=total_items,
        has_previous=page > 1,
        has_next=page < total_pages,
        scope=scope,
        scopes=scopes,
        path=request.args.get("path", "")
    )