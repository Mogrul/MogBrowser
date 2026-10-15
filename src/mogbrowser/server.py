from pathlib import Path

from flask import Flask, render_template

from .routes import register_blueprints

class Server:
    def __init__(self):
        self.app = Flask(
            __name__,
            template_folder=Path("src/templates").resolve(),
        )

        register_blueprints(self.app)

    def run(self):
        self.app.run(
            host="0.0.0.0",
            port=5000,
            debug=True,
        )

    def gallery(self):
        pass