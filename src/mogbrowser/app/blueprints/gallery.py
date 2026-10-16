from pathlib import Path, PurePosixPath

from click import option
from quart import Blueprint, render_template, request

from mogbrowser import config, get_path_type
from mogbrowser.app import Responses

gallery = Blueprint("gallery", __name__)

@gallery.route("/", methods=["GET"])
async def index():
    scope_target = request.args.get("scope", "root")
    path_target = request.args.get("path", "")

    if scope_target not in config.scopes:
        return Responses.send_fail(f"Scope ({scope_target}) doesn't exist")

    if (target_scope_path := config.scopes[scope_target].get("path")) is None:
        return Responses.send_fail(f"Failed to get path from scope ({scope_target})")

    full_target_path = (
        Path(target_scope_path)
        if path_target == target_scope_path
        else Path(f"{target_scope_path}/{path_target}")
    )

    if not full_target_path.exists():
        return Responses.send_fail(f"Failed to get full path from scope ({scope_target}) and ({path_target})")

    paths = []
    for path in full_target_path.iterdir():
        paths.append({"name": path.name, "type": get_path_type(path)})

    return await render_template(
        "gallery.html",
        current_scope=str(PurePosixPath(scope_target)),
        current_path=str(PurePosixPath(path_target)),
        paths=paths,
        scopes=config.scopes.keys()
    )