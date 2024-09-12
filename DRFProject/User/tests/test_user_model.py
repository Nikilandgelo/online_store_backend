import pytest
from User.models import User
from django.core.exceptions import ValidationError


@pytest.fixture
def user_data() -> dict[str, str]:
    return {
        "username": "testuser",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "password": "password123"
    }


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self, user_data: dict[str, str]):
        user: User = User.objects.create(**user_data)
        assert user.username == user_data.get("username")
        assert user.first_name == user_data.get("first_name")
        assert user.last_name == user_data.get("last_name")
        assert user.email == user_data.get("email")
        assert user.password == user_data.get('password')
        assert user.is_email_confirm is False
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_email_unique(self, user_data):
        User.objects.create(**user_data)
        user_data["username"] = "testuser2"
        with pytest.raises(Exception):
            User.objects.create_user(**user_data)

    def test_update_email_confirm(self, user_data):
        user: User = User.objects.create(**user_data)
        assert user.is_email_confirm is False

        user.is_email_confirm = True
        user.save()

        updated_user: User = User.objects.get(
            username=user_data.get("username"))
        assert updated_user.is_email_confirm is True

    def test_username_length_limit(self):
        user: User = User.objects.create(
            username="a" * 150,
            first_name="a" * 70,
            last_name="b" * 70,
            email="longnametest@example.com",
            password="password123"
        )
        assert user.username == "a" * 150
        assert len(user.first_name) == 70
        assert len(user.last_name) == 70

    def test_create_user_without_username(self, user_data):
        user_data['username'] = ""
        user: User = User.objects.create(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_create_user_without_email(self, user_data):
        user_data['email'] = ""
        user: User = User.objects.create(**user_data)
        with pytest.raises(ValidationError):
            user.full_clean()

    def test_user_str(self, user_data):
        user: User = User.objects.create(**user_data)
        assert str(user) == user_data.get("username")

    def test_email_case_insensitivity(self, user_data):
        user_data['email'] = 'TomSmith@example.com'
        User.objects.create(**user_data)
        with pytest.raises(Exception):
            User.objects.create(
                username="testuser7",
                first_name="Jerry",
                last_name="Jones",
                email="tomsmith@example.com",
                password="password123"
            )

    def test_user_deletion(self, user_data):
        user: User = User.objects.create(**user_data)
        user_id = user.id
        user.delete()

        with pytest.raises(User.DoesNotExist):
            User.objects.get(id=user_id)

    def test_create_superuser(self):
        user: User = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="adminpass123"
        )
        assert user.is_superuser is True
        assert user.is_staff is True
