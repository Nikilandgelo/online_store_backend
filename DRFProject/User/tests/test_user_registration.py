import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from User.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_data, expected_status, expected_message_key, expected_message_value",
    [
        # Regular valid input
        (
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'supersecretpassword'
            },
            201,
            None,
            ('User has been created, now you will get a message with '
             'confirmation, please verify your email address.')
        ),
        # Empty first name
        (
            {
                'first_name': '',
                'last_name': 'Doe',
                'email': 'empty_first@example.com',
                'password': 'supersecretpassword'
            },
            400,
            'first_name',
            'This field may not be blank.'
        ),
        # Long last name
        (
            {
                'first_name': 'John',
                'last_name': 'Doe' * 24,
                'email': 'long_last@example.com',
                'password': 'supersecretpassword'
            },
            400,
            'last_name',
            'Ensure this field has no more than 70 characters.'
        ),
        # Invalid email format
        (
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'invalid-email',
                'password': 'supersecretpassword'
            },
            400,
            'email',
            'Enter a valid email address.'
        ),
        # Short password
        (
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'short_pass@example.com',
                'password': '123'
            },
            400,
            'password',
            ('This password is too short. It must contain at least '
             '8 characters.')
        ),
        # Common password
        (
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'common_pass@example.com',
                'password': 'password'
            },
            400,
            'password',
            'This password is too common.'
        ),
        # Missing email
        (
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'supersecretpassword'
            },
            400,
            'email',
            'This field is required.'
        ),
        # Invalid first name or last name (numbers)
        (
            {
                'first_name': 'John123',
                'last_name': 'Doe',
                'email': 'invalid_name@example.com',
                'password': 'supersecretpassword'
            },
            400,
            'first_name and last_name',
            'First name and last name can not contain numbers.'
        ),
        # Valid data with special characters in name
        (
            {
                'first_name': 'John',
                'last_name': 'O\'Connor',
                'email': 'special_char@example.com',
                'password': 'supersecretpassword'
            },
            201,
            None,
            ('User has been created, now you will get a message with '
             'confirmation, please verify your email address.')
        )
    ]
)
def test_register_user(user_data: dict[str, str],
                       expected_status,
                       expected_message_key,
                       expected_message_value):

    response = APIClient().post(reverse('registration_user'), user_data)
    assert response.status_code == expected_status
    if response.status_code == 201:
        assert response.data == expected_message_value
        user: User = User.objects.get(email=user_data['email'])
        assert user.first_name == user_data['first_name']
        assert user.last_name == user_data['last_name']
        assert check_password(user_data['password'], user.password)
        token: Token = Token.objects.get(user=user)
        assert token is not None
    else:
        assert expected_message_key in response.data
        assert response.data[expected_message_key][0] == expected_message_value
