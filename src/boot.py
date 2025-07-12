from flask import Flask

from hooks import init_hooks
from logger import init_logger
from routes import init_routes
from sockets import init_sockets


def init(app: Flask):
    if hasattr(app, "socket") and app.socket:
        return

    @app.context_processor
    def inject_build():
        from config import Config

        return {"build": Config.get_build()}

    init_logger(app)
    init_hooks(app)
    init_routes(app)
    app.socket = init_sockets(app)

    return app.socket
