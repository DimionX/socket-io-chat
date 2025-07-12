import uuid

from flask import Flask, redirect, render_template, request, session, url_for

import utils
from messages import failed_login, success_login
from utils import generate_qr_code, generate_totp_uri


def init_routes(app: Flask):
    from config import Config

    limiter = Config.get_limiter(app)

    @app.route("/", endpoint="index")
    def index():
        chat_id = str(uuid.uuid4().hex)
        qr_url = f"{Config.SERVER_URL}/chat/{chat_id}"
        qr_code = generate_qr_code(qr_url)

        return render_template("index.html", chat_id=chat_id, qr_code=qr_code)

    @app.route("/totp")
    def totp():
        otp_uri = generate_totp_uri()
        qr_code = generate_qr_code(otp_uri)

        with open(Config.TOTP_USED_PATH, "w") as f:
            f.write("used")

        return render_template("totp.html", qr_code=qr_code)

    @app.route("/auth", methods=["GET", "POST"])
    @limiter.limit("5 per minute", methods=["POST"])
    def auth():
        if request.method == "GET":
            return render_template("totp_auth.html")

        code = request.form.get("code")
        user_ip = request.remote_addr
        user_agent = request.headers.get("User-Agent", "unknown")

        if utils.get_totp().verify(code):
            session["authenticated"] = True
            next_url = request.args.get("next") or url_for("index")
            app.logger.info(**success_login(user_ip, user_agent))
            return redirect(next_url)

        app.logger.warning(**failed_login(user_ip, user_agent, code))

        return render_template("auth_failed.html")

    @app.route("/chat/<chat_id>")
    def chat(chat_id: str):
        return render_template("chat.html", chat_id=chat_id)

    @app.errorhandler(404)
    def handle_404(error):
        return render_template("404.html"), 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return render_template("429.html"), 429

    @app.route("/health")
    def health_check():
        return {"status": "healthy"}, 200
