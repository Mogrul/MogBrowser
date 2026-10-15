from pathlib import Path

from flask import Blueprint, render_template, request, abort, send_file

media = Blueprint("media", __name__, url_prefix="/media")

from mogbrowser import scopes, thumbnail_path

@media.route("/file")
def file():
    path = request.args.get("path")
    scope = request.args.get("scope")

    if scope not in scopes:
        return abort(404)

    if not path:
        return abort(404)

    file_path = Path(path).resolve()

    return send_file(file_path)

@media.route("/thumbnail")
def thumbnail():
    path_id = request.args.get("id")

    if not path_id:
        return abort(404)

    full_path = (thumbnail_path / (path_id + ".webp")).resolve()

    if not full_path.is_file():
        return abort(404)

    return send_file(full_path)