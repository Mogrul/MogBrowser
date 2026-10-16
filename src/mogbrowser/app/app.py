import asyncio
from pathlib import Path

from quart import Quart

from mogbrowser.config import config
from mogbrowser.app.blueprints import gallery, media, events

class App(Quart):
    def __init__(self):
        super().__init__(
            import_name="app",
            static_folder=str(Path("data/static").resolve()),
            template_folder=str(Path("data/templates").resolve()),
        )

        self.register_blueprint(gallery)
        self.register_blueprint(media)
        self.register_blueprint(events)

    def start(self) -> None:
        self.run(
            host="0.0.0.0",
            port=5000,
            debug=config.debug,
        )