from rest_framework.serializers import (
    Serializer, ModelSerializer, EmailField, CharField)
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
import re
from rest_framework.serializers import ValidationError


class LoginSerializer(Serializer):
    """
    Serializer class for user login.

    This class is used to serialize the user email and password
    received from the client for user authentication.
    """
    email = EmailField(help_text="The user's email address.")
    password = CharField(max_length=128, help_text="The user's password.")


class RegistrationSerializer(ModelSerializer):
    """
    Serializer class for user registration.

    This class is used to serialize the user's first name, last name, email,
    and password. It also hashes the password and generates a unique username
    based on the first name and last name.
    """

    class Meta:
        model = User
        fields: list[str] = ['first_name', 'last_name', 'email', 'password']

    def validate(self, attrs: dict):
        if (re.search(r'\d', attrs.get('first_name')) is not None or
                re.search(r'\d', attrs.get('last_name')) is not None):
            raise ValidationError(
                {"first_name and last_name":
                 'First name and last name can not contain numbers.'})
        return attrs

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value

    def create(self, validated_data: dict) -> User:
        """
        This function extends the default create function of the
        ModelSerializer. It creates a new user with a unique username based
        on the first name and last name. The username is created in the format:
        first_name-last_name_1, first_name-last_name_2, etc.
        """
        username_pattern: str = (f'{validated_data.get("first_name")}-'
                                 f'{validated_data.get("last_name")}')
        last_user = User.objects.filter(
            username__istartswith=username_pattern).order_by('-username')
        last_user: User | None = last_user.first()
        if last_user is not None:
            counter = int(last_user.username.split('_')[-1]) + 1
        else:
            counter: int = 1

        validated_data['username'] = f'{username_pattern}_{counter}'
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
