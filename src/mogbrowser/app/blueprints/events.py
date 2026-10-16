from quart import Response, Blueprint

from mogbrowser.app import event_manager

events = Blueprint("events", __name__, url_prefix="/events")

@events.route("")
async def event():
    return Response(
        event_manager.subscribe(),
        content_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )