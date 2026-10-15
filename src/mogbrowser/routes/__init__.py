from flask import Flask

from .home import home
from .media import media

def register_blueprints(app: Flask):
    app.register_blueprint(home)
    app.register_blueprint(media)