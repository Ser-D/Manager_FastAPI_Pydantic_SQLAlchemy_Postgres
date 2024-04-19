import pytest

from unittest.mock import Mock, patch, AsyncMock
from sqlalchemy import select
from tests.conftest import TestingSessionLocal
from src.conf import messages

from src.contacts.models import User
from src.services.auth import auth_service
from tests.conftest import TestingSessionLocal, test_user

user_data = {"username": "Alarm", "email": "Alarm@example.com", "password": "12345678"}


def test_signup(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.users.routes.send_email", mock_send_email)
    response = client.post("/auth/signup", json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "password" not in data
    assert "avatar" in data


def test_repeat_signup(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.users.routes.send_email", mock_send_email)
    response = client.post("/auth/signup", json=user_data)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == messages.ACCOUNT_EXIST


def test_not_confirmed_login(client):
    response = client.post("/auth/login",
                           data={"username": user_data.get("email"), "password": user_data.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == messages.NOT_CONFIRM
