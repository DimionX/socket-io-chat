from flask import Flask

app = Flask(__name__, static_url_path="", static_folder="public", template_folder="templates")

if __name__ == "__main__":
    from boot import init
    from config import Config

    app.secret_key = Config.FLASK_SECRET_KEY
    socketio = init(app)

    socketio.run(app, host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, use_reloader=True)
