import os

import pyotp

secret = os.getenv("TOTP_SECRET")
if not secret:
    secret = pyotp.random_base32()

with open("/home/user/secrets/totp", "w") as f:
    f.write(secret)
