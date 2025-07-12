import base64
import os

key = base64.urlsafe_b64encode(os.urandom(32)).decode()
with open("/home/user/secrets/flask", "w") as f:
    f.write(key)
