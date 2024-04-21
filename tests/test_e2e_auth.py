import pytest

from unittest.mock import Mock, patch, AsyncMock
from sqlalchemy import select
from src.conf import messages

from src.contacts.models import User
from conftest import sessionmanager

user_data = {"username": "Alarm", "email": "Alarm@example.com", "password": "12345678"}


def test_signup(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("src.users.routes.send_email", mock_send_email)
    response = client.post("auth/signup", json=user_data)
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


@pytest.mark.asyncio
async def test_login(client):
    async with sessionmanager.session() as session:
        current_user = await session.execute(
            select(User).where(User.email == user_data.get("email"))
        )
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.confirmed = True
            await session.commit()

    response = client.post("/auth/login",
                           data={"username": user_data.get("email"), "password": user_data.get("password")})
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


def test_wrong_password_login(client, monkeypatch):
    response = client.post("auth/login",
                           data={"username": user_data.get("email"), "password": "password"})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == messages.INVALID_CREDENTIALS


def test_wrong_email_login(client):
    response = client.post("auth/login",
                           data={"username": "email", "password": user_data.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == messages.INVALID_CREDENTIALS


def test_validation_error_login(client, monkeypatch):
    response = client.post("auth/login",
                           data={"password": user_data.get("password")})
    assert response.status_code == 422, response.text
    data = response.json()
    assert "detail" in data
