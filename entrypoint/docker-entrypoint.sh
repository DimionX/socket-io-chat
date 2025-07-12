#!/usr/bin/env bash
set -e

# FLASK_SECRET_KEY
if [ ! -f /home/user/secrets/flask ]; then
  python /tmp/entrypoint/flask.py
fi

# TOTP_SECRET
if [ ! -f /workspace/secrets/totp ]; then
  python /tmp/entrypoint/totp.py
fi

export FLASK_SECRET_KEY="$(cat /home/user/secrets/flask)"
export TOTP_SECRET="$(cat /home/user/secrets/totp)"

python app.py
