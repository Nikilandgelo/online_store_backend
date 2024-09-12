import pytest
from User.models import User
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.hashers import make_password


@pytest.fixture
def create_user() -> User:
    return User.objects.create(
        username="testuser",
        first_name="Test",
        last_name="User",
        email="testuser@example.com",
        password=make_password("password123")
    )


@pytest.mark.parametrize(
    'data, status_code, expected_data, token',
    [
        (
            {'email': 'testuser@example.com', 'password': 'password123'},
            200,
            ('Hello Test! You are proofed that you are registered. '
             'Your token is in headers.'),
            True
        ),
        (
            {'email': 'wrongemail@example.com', 'password': 'password123'},
            404,
            {'detail': 'No User matches the given query.'},
            False
        ),
        (
            {'email': 'testuser@example.com', 'password': 'wrongpassword123'},
            400,
            'Password is not correct',
            False
        ),
        (
            {},
            400,
            {"email": ["This field is required."],
             "password": ["This field is required."]},
            False
        )
    ]
)
@pytest.mark.django_db
def test_login_with_valid_credentials(create_user: User, data: dict[str, str],
                                      status_code: int, expected_data,
                                      token: bool):
    response = APIClient().post(f'{reverse("login_user")}', data=data)

    assert response.status_code == status_code
    assert response.data == expected_data

    if token:
        assert 'Authorization' in response.headers
        assert response.headers['Authorization'].startswith('Token ')
