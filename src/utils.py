import base64
from io import BytesIO

import qrcode
from pyotp import TOTP


def generate_qr_code(text: str) -> str:
    """QR code generation and saving"""
    img = qrcode.make(text)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{img_base64}"


def get_totp() -> TOTP:
    from config import Config

    return TOTP(Config.TOTP_SECRET)


def generate_totp_uri() -> str:
    from config import Config

    return get_totp().provisioning_uri(name=Config.TOTP_USER, issuer_name=Config.TOTP_ISSUER_NAME)
