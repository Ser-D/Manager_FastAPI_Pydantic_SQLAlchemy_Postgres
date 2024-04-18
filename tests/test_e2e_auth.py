import pytest

from unittest.mock import Mock, patch, AsyncMock
from sqlalchemy import select
from tests.conftest import TestingSessionLocal

from src.contacts.models import User
from src.services.auth import auth_service
from tests.conftest import TestingSessionLocal, test_user

user_data = {"username": "Alarm", "email": "Alarm@example.com", "password": "12345678"}


def test_signup(client, monkeypatch):

        mock_send_email = Mock()
        monkeypatch.setattr("src.services.email.send_email", mock_send_email)
        response = client.post("auth/signup", json=user_data)
        assert response.status_code == 409, response.text
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert "password" not in data
        assert "avatar" in data
        assert mock_send_email.called
