import pytest
from django.contrib.auth.hashers import make_password
from User.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.hashers import check_password


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "password": make_password("password123")
    }


@pytest.fixture
def create_user(user_data):
    user: User = User.objects.create(**user_data)
    token: Token = Token.objects.get(user=user)
    return user, token


@pytest.mark.django_db
@pytest.mark.parametrize("email, expected_status, expected_data",
                         [
                             ("johndoe@example.com", 200, "Check your email"),
                             ("invalidemail@example.com", 404,
                              {"detail": "No User matches the given query."}),
                         ])
def test_reset_password_view_post(create_user, email,
                                  expected_status, expected_data):
    response = APIClient().post(
        reverse('ask_reset_password'), {"email": email})

    assert response.status_code == expected_status
    assert response.data == expected_data


@pytest.mark.django_db
@pytest.mark.parametrize("token, password, expected_status, expected_data",
                         [
                             ("Correct", "testtesttest", 200,
                              "Password has been changed"),
                             ("Wrong", "superhardpassword", 404,
                              {"detail": "No Token matches the given query."}
                              ),
                             ("Correct", "", 400, "Please enter new password"),
                             ("Correct", "password", 400,
                              "This password is too common."
                              ),
                         ])
def test_change_password_valid(create_user: tuple[User, Token], token: str,
                               password: str, expected_status: int,
                               expected_data: str):
    if token == "Correct":
        token = create_user[1].key
    response = APIClient().post(
        f'{reverse("change_password")}?token={token}', {"password": password})

    assert response.status_code == expected_status
    assert response.data == expected_data
    if expected_status == 200:
        create_user[0].refresh_from_db()
        assert check_password(password, create_user[0].password) is True
