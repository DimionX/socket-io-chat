def test_totp_route(client, mocker):
    # Mock TOTP as not configured
    mocker.patch("os.path.exists", return_value=False)

    response = client.get("/totp")
    assert response.status_code == 200


def test_successful_auth(client, mocker, app):
    # Mock successful TOTP verification
    mock_totp = mocker.Mock(verify=mocker.Mock(return_value=True))
    mocker.patch("utils.get_totp", return_value=mock_totp)

    with app.test_request_context():
        response = client.post("/auth", data={"code": "123456"})
        assert response.status_code == 302

        with client.session_transaction() as session:
            assert session["authenticated"] is True


def test_failed_auth(client, mocker):
    # Mock failed TOTP verification
    mock_totp = mocker.Mock(verify=mocker.Mock(return_value=False))
    mocker.patch("utils.get_totp", return_value=mock_totp)

    response = client.post("/auth", data={"code": "654321"})
    assert response.status_code == 200
    assert b"Authentication Failed" in response.data
