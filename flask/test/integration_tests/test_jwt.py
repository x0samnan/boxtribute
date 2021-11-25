"""Verify JWT handling when sending a request to the Flask app.
These tests fetch actual authentication data from the Auth0 web service and hence
require a working internet connection.
"""
import os

import pytest
from auth import get_user_token_string
from boxtribute_server.auth import (
    decode_jwt,
    get_public_key,
    get_token_from_auth_header,
)


def test_expired_jwt(client):
    client.environ_base[
        "HTTP_AUTHORIZATION"
    ] = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJYZFQzNFlvTlVBdTRlbG9Xd1B2ZSJ9.eyJodHRwczovL3d3dy5ib3h0cmlidXRlLmNvbS9lbWFpbCI6ImRldl9jb29yZGluYXRvckBib3hhaWQub3JnIiwiaHR0cHM6Ly93d3cuYm94dHJpYnV0ZS5jb20vYmFzZV9pZHMiOlsiMSJdLCJodHRwczovL3d3dy5ib3h0cmlidXRlLmNvbS9vcmdhbmlzYXRpb25faWQiOiIxIiwiaXNzIjoiaHR0cHM6Ly9ib3h0cmlidXRlLWRldi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8OCIsImF1ZCI6ImJveHRyaWJ1dGUtZGV2LWFwaSIsImlhdCI6MTYzMzQyNzk0OCwiZXhwIjoxNjMzNTE0MzQ4LCJhenAiOiJaa3N2aDVOUDQyQ0dOMTJZaGdhWWYwV2YyTFNBTTJQaCIsImd0eSI6InBhc3N3b3JkIiwicGVybWlzc2lvbnMiOltdfQ.xw0le_T7yqDPtRu31Hu_7H3MwdbVE1vDvxYwJEpy5wuzhjD2oQyCijG8tWsqo7vqaj0KwVDywKDqOotBgfTi5uA_Sk3emNYtZCNBjBLpz4IQQpGwzI84xECU3CR6HKzWQ5rUs5RYaM4DqyKjiQ4XQPqrJQNI9Q-WRsbhbIo6LY1pEu5YcwXwsYhSxZLadfGosjHJpb5BlXSIMdPEWb0O0TuqxmKQMAcFJ4ffFZH1_saCry62DSAl7dy5DfROtmbqP7gGxgvywodUvo4VxrVNSZkWp5k1wOzNNlK1Jl58yXLeM9UCFgKRmK2KNVAJW1st01GjiRhafycKUEcx4Ftfsw"  # noqa
    response = client.post("/graphql")
    assert response.status_code == 401
    assert response.json["code"] == "token_expired"


@pytest.mark.skipif("CIRCLECI" not in os.environ, reason="only functional in CircleCI")
def test_invalid_jwt_claims(auth0_client, monkeypatch):
    monkeypatch.setenv("AUTH0_AUDIENCE", "invalid-audience")
    response = auth0_client.post("/graphql")
    assert response.status_code == 401
    assert response.json["code"] == "invalid_claims"


def test_decode_valid_jwt():
    token = get_token_from_auth_header(get_user_token_string())
    key = get_public_key()
    assert key is not None
    assert decode_jwt(token, key) is not None
