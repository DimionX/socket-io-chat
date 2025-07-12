import os

from flask import Flask, abort, redirect, request, session, url_for


def init_hooks(app: Flask):
    from config import Config

    @app.before_request
    def enforce_authentication():
        path = request.path
        endpoint = request.endpoint or ""
        qr_is_used = os.path.exists(Config.TOTP_USED_PATH)

        if path in ("/health", "/favicon.ico") or path.startswith("/static/") or path.startswith("/assets/"):
            return

        if endpoint == "totp":
            if qr_is_used:
                abort(403, description="TOTP setup already completed")

            return

        if not qr_is_used:
            return redirect(url_for("totp", next=path))

        if path.startswith("/auth"):
            return

        if not session.get("authenticated"):
            return redirect(url_for("auth", next=path))
