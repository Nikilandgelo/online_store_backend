import pytest
from User.serializers import RegistrationSerializer
from User.models import User
from django.contrib.auth.hashers import check_password
from django.db.models import Model


@pytest.fixture
def user_data() -> dict[str, str]:
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "password": "password123!"
    }


@pytest.fixture
def serializer(user_data: dict[str, str]) -> RegistrationSerializer:
    return RegistrationSerializer(data=user_data)


@pytest.mark.django_db
def test_registration_serializer_valid_data(
        user_data, serializer: RegistrationSerializer):
    assert serializer.is_valid() is True
    user: Model = serializer.save()

    assert User.objects.count() == 1
    assert user.username == (f'{user_data.get("first_name")}'
                             f'-{user_data.get("last_name")}_1')
    assert check_password(user_data.get('password'), user.password) is True
    assert user.email == user_data.get('email')


@pytest.mark.django_db
def test_registration_serializer_invalid_first_name(user_data):
    user_data['first_name'] = 'John1'
    serializer = RegistrationSerializer(data=user_data)

    assert serializer.is_valid() is False
    assert 'first_name and last_name' in serializer.errors
    assert serializer.errors['first_name and last_name'][0] == (
        'First name and last name can not contain numbers.')


@pytest.mark.django_db
def test_registration_serializer_invalid_last_name(user_data):
    user_data['last_name'] = 'Doe2'
    serializer = RegistrationSerializer(data=user_data)

    assert serializer.is_valid() is False
    assert 'first_name and last_name' in serializer.errors
    assert serializer.errors['first_name and last_name'][0] == (
        'First name and last name can not contain numbers.')


@pytest.mark.django_db
def test_registration_serializer_empty_first_name(user_data):
    user_data['first_name'] = '   '  # Only spaces
    serializer = RegistrationSerializer(data=user_data)

    assert serializer.is_valid() is False
    assert 'first_name' in serializer.errors
    assert serializer.errors['first_name'][0] == "This field may not be blank."


@pytest.mark.django_db
def test_registration_serializer_password_validation(user_data):
    user_data['password'] = '1234'  # Too simple
    serializer = RegistrationSerializer(data=user_data)

    assert serializer.is_valid() is False
    assert 'password' in serializer.errors


@pytest.mark.django_db
def test_registration_serializer_email_validation(user_data):
    user_data['email'] = 'invalid-email'  # Invalid email format
    serializer = RegistrationSerializer(data=user_data)

    assert serializer.is_valid() is False
    assert 'email' in serializer.errors
    assert serializer.errors['email'][0] == 'Enter a valid email address.'


@pytest.mark.django_db
def test_registration_serializer_username_uniqueness(
        user_data, serializer: RegistrationSerializer):
    assert serializer.is_valid() is True
    user: Model = serializer.save()

    user_data['email'] = 'johndoe2@example.com'
    second_serializer = RegistrationSerializer(data=user_data)

    assert second_serializer.is_valid() is True
    user: User = second_serializer.save()

    assert user.username == 'John-Doe_2'
