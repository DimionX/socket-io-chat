from datetime import datetime, timezone

from flask import Flask
from flask_socketio import SocketIO, emit, join_room


def init_sockets(app: Flask):
    socketio = SocketIO(app)

    @socketio.on("join")
    def on_join(data):
        join_room(data.get("chat_id"))

    @socketio.on("typing")
    def handle_typing(data):
        chat_id = data.get("chat_id")
        emit("show_typing", {}, room=chat_id, include_self=False)

    @socketio.on("stop_typing")
    def handle_stop_typing(data):
        emit("hide_typing", {}, room=data.get("chat_id"), include_self=False)

    @socketio.on("send_message")
    def handle_message(data):
        timestamp = datetime.now(timezone.utc).isoformat()
        emit(
            "receive_message",
            {"message": data.get("message"), "timestamp": timestamp},
            room=data.get("chat_id"),
            include_self=False,
        )

    return socketio
