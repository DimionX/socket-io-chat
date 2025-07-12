def test_unauthenticated_redirect(client, mocker):
    # Mock TOTP as configured
    mocker.patch("os.path.exists", return_value=True)

    # Access protected route without auth
    response = client.get("/chat/test")
    assert response.status_code == 302
    assert "/auth" in response.location


def test_totp_redirect(client, mocker):
    # Mock TOTP as not configured
    mocker.patch("os.path.exists", return_value=False)

    # Should redirect to TOTP setup
    response = client.get("/")
    assert response.status_code == 302
    assert "/totp" in response.location
