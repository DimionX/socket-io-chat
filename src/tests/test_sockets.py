from flask_socketio import SocketIOTestClient


def test_message_handling(app):
    clients = (
        SocketIOTestClient(app, app.socket),
        SocketIOTestClient(app, app.socket),
    )

    messages = [], []
    for client in clients:
        client.connect()
        client.emit("join", {"chat_id": "test_room"})

    clients[0].emit("send_message", {"message": "[1] First message", "chat_id": "test_room"})
    clients[1].emit("send_message", {"message": "[2] First message", "chat_id": "test_room"})
    clients[0].emit("send_message", {"message": "[1] Second message", "chat_id": "test_room"})

    for client, received in zip(clients, messages):
        received.extend(client.get_received())

    # First client
    received = messages[0]
    assert len(received) == 1
    assert received[0]["args"][0]["message"] == "[2] First message"
    assert "timestamp" in received[0]["args"][0]

    # Second client
    received = messages[1]
    assert len(received) == 2
    assert received[0]["name"] == "receive_message"
    assert received[0]["args"][0]["message"] == "[1] First message"
    assert received[1]["args"][0]["message"] == "[1] Second message"
    assert "timestamp" in received[0]["args"][0]

    for client in clients:
        client.disconnect()
