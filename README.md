# Socket.IO Chat with TOTP Authentication

A web chat application featuring two-factor authentication (TOTP), real-time messaging, and image sharing.
Built with Flask and Socket.IO, protected against brute-force attacks using Redis rate limiting.

## ✨ Key Features
- 🔐 **TOTP Authentication** via Google Authenticator
- 📨 **Real-time messaging** with Socket.IO
- 👀 **Typing indicators** showing user activity
- 🤖 **Telegram integration** for critical alerts
- 🛡️ **Brute-force protection** with Redis rate limiting
- 📊 **JSON logging** with file rotation and Telegram notifications

## ⚙️ Technology Stack

| Component | Technologies |
|-----------|--------------|
| **Backend** | Python 3.12, Flask, Flask-SocketIO |
| **Frontend** | JS, SCSS, Socket.IO Client |
| **Security** | PyOTP, Flask-Limiter |
| **Infrastructure** | Docker, Redis |

## 🚀 Quick Start

### Launch Application

```bash
git clone https://github.com/DimionX/socket-io-chat.git
cd socket-io-chat

# Create .env configuration
cp .env.example .env

# Start services
docker compose up --build
```

Access at: http://127.0.0.1:5000

### Initial Setup

1. Open http://127.0.0.1:5000
2. System will redirect to TOTP setup page
3. Scan QR code with authenticator app
4. Authenticate using generated codes

## 🔧 Configuration (.env)

```ini
# [APP]
SERVER_URL=http://127.0.0.1:5000
STORAGE_LIMITER="redis://redis:6379/0"

# [TOTP]
TOTP_SECRET=  # Auto-generated on first run
TOTP_USER="chat_user"
TOTP_ISSUER_NAME="Secure Chat"

# [Telegram]
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 🌐 Socket.IO Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `join` | Client → Server | Join chat room |
| `typing` | Client → Server | User is typing |
| `stop_typing` | Client → Server | User stopped typing |
| `send_message` | Client → Server | Send new message |
| `receive_message` | Server → Client | Broadcast new message |


## 📂 Project Structure

| Path            | Description |
|-----------------|-------------|
| `src/boot.py`   | Application initialization |
| `src/hooks.py`  | Authentication and route protection |
| `src/logger.py` | JSON logging with Telegram integration |
| `src/routes.py` | Flask endpoints with rate limiting |
| `src/sockets.py` | Socket.IO event handlers |
| `src/utils.py`  | TOTP and QR code utilities |
| `entrypoint/`   | Docker initialization scripts |

