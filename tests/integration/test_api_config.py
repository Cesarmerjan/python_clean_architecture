from flask import current_app, request


def test_api_config(api):
    assert current_app is not None
    assert current_app.config["TESTING"]
