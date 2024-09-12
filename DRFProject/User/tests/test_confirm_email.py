import pytest
from User.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def create_user() -> User:
    user: User = User.objects.create(
        username="testuser",
        first_name="Test",
        last_name="User",
        email="testuser@example.com",
        password="password123",
    )
    return user


@pytest.fixture
def token(create_user: User) -> Token:
    return Token.objects.get(user=create_user)


@pytest.mark.django_db
def test_confirm_email_with_valid_token(token: Token):
    response = APIClient().get(
        f'{reverse("registration_user")}?token={token.key}')

    assert response.status_code == 200
    assert response.data == 'User has been confirmed'

    user: User = token.user
    user.refresh_from_db()
    assert user.is_email_confirm is True


@pytest.mark.django_db
def test_confirm_email_with_invalid_token():
    response = APIClient().get(
        f'{reverse("registration_user")}?token=1234567890abcdef')

    assert response.status_code == 404
    assert response.data == {'detail': 'No Token matches the given query.'}


@pytest.mark.django_db
def test_confirm_email_with_missing_token():
    response = APIClient().get(f'{reverse("registration_user")}')

    assert response.status_code == 404
    assert response.data == {'detail': 'No Token matches the given query.'}


@pytest.mark.django_db
def test_confirm_email_with_already_confirmed_email(create_user: User,
                                                    token: Token):
    create_user.is_email_confirm = True
    create_user.save()

    response = APIClient().get(
        f'{reverse("registration_user")}?token={token.key}')

    assert response.status_code == 400
    assert response.data == 'User is already confirmed'


@pytest.mark.django_db
def test_confirm_email_with_malformed_token():
    response = APIClient().get(
        f'{reverse("registration_user")}?token=invalidtoken!@#')

    assert response.status_code == 404
    assert response.data == {'detail': 'No Token matches the given query.'}
