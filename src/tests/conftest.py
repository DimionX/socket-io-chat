import os
import tempfile

import pytest

from app import app as flask_app
from boot import init


def pytest_configure(config):
    os.environ["STORAGE_LIMITER"] = "memory://"
    os.environ["TOTP_SECRET"] = "JBSWY3DPEHPK3PXP"
    os.environ["TOTP_USER"] = "test_user"
    os.environ["TOTP_ISSUER_NAME"] = "Test Chat"
    os.environ["TELEGRAM_BOT_TOKEN"] = ""
    os.environ["TELEGRAM_CHAT_ID"] = ""


@pytest.fixture(scope="session", autouse=True)
def session():
    # Create a temporary file for TOTP marker
    _, totp_used_path = tempfile.mkstemp()
    os.environ["TOTP_USED_PATH"] = totp_used_path

    yield

    os.unlink(os.getenv("TOTP_USED_PATH"))


@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for each test module."""

    # Configure application
    flask_app.config.update(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
        }
    )

    # Initialize application components
    init(flask_app)
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture(autouse=True)
def clear_session(client):
    """Clear session before each test."""
    with client.session_transaction() as session:
        session.clear()
