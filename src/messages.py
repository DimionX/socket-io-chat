from typing import Optional


def success_login(user_ip: str, user_agent: str) -> dict:
    return {
        "msg": "✅ Successful TOTP login",
        "extra": {
            "ip": user_ip,
            "user_agent": user_agent,
        },
    }


def failed_login(user_ip: str, user_agent: str, otp: Optional[str]) -> dict:
    return {
        "msg": "❌ Failed TOTP login attempt!",
        "extra": {
            "ip": user_ip,
            "user_agent": user_agent,
            "code": otp,
        },
    }
