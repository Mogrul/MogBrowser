from pathlib import Path

from quart import Blueprint, send_file, request

from mogbrowser import config
from mogbrowser.app import Responses

media = Blueprint("media", __name__, url_prefix="/media")

@media.route("/", methods=["GET"])
async def file():
    scope_target = request.args.get("scope")
    path_target = request.args.get("path")

    if scope_target is None:
        return Responses.send_fail("No scope specified")

    if path_target is None:
        return Responses.send_fail("No path specified")

    if (target_scope_path := config.scopes[scope_target].get("path")) is None:
        return Responses.send_fail(f"Failed to get path from scope ({scope_target})")

    full_target_path = (
        Path(target_scope_path)
        if path_target == target_scope_path
        else Path(f"{target_scope_path}/{path_target}")
    )

    if not full_target_path.exists() or not full_target_path.is_file():
        return Responses.send_fail(f"Failed to get full path from scope ({scope_target}) and ({path_target})")

    return await send_file(full_target_path, conditional=True)

@media.route("/thumbnail", methods=["POST"])
async def get_thumbnail():
    data = await request.get_json()
    target_scope = data.get("scope")
    target_paths = data.get("paths", [])

    if not target_scope:
        return Responses.send_fail("No scope provided", 400)

    if not target_paths:
        return Responses.send_fail("Invalid or no paths provided", 400)

    if (
        not (scope_path := config.scopes.get(target_scope, {}).get("path"))
        or not (scope_path := Path(scope_path)).exists()
    ):
        return Responses.send_fail("Scope not found")

    paths = [
        scope_path / path
        for path in target_paths
    ]

    return {
        "success": True,
        "requested": len(paths)
    }