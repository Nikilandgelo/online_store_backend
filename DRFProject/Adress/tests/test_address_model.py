import pytest
from User.models import User
from Adress.models import Address
from django.core.exceptions import ValidationError


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="password123",
        first_name="John",
        last_name="Doe"
    )


@pytest.fixture
def address_data(user: User) -> dict:
    return {
        "user": user,
        "city": "Test City",
        "street": "Test Street",
        "house_number": 123,
        "hull_building": "A",
        "apartment": 10,
    }


@pytest.mark.django_db
class TestAddressModel:

    def test_create_address(self, address_data: dict[str, any]):
        address: Address = Address.objects.create(**address_data)
        assert address.user == address_data["user"]
        assert address.city == address_data["city"]
        assert address.street == address_data["street"]
        assert address.house_number == address_data["house_number"]
        assert address.hull_building == address_data["hull_building"]
        assert address.apartment == address_data["apartment"]

    def test_unique_constraint(self, address_data: dict[str, any]):
        Address.objects.create(**address_data)
        with pytest.raises(ValidationError):
            address = Address(**address_data)
            address.full_clean()

    def test_non_unique_with_different_apartment(self,
                                                 address_data: dict[str, any]):
        Address.objects.create(**address_data)
        address_data['apartment'] = 11
        address: Address = Address.objects.create(**address_data)
        assert address.apartment == 11

    def test_blank_hull_building(self, address_data: dict[str, any]):
        address_data['hull_building'] = ""
        address: Address = Address.objects.create(**address_data)
        assert address.hull_building == ""

    def test_invalid_city_name(self, address_data: dict[str, any]):
        address_data['city'] = ""
        address = Address(**address_data)
        with pytest.raises(ValidationError):
            address.full_clean()

    def test_invalid_house_number(self, address_data: dict[str, any]):
        address_data['house_number'] = -1
        address = Address(**address_data)
        with pytest.raises(ValidationError):
            address.full_clean()

    def test_invalid_apartment_number(self, address_data: dict[str, any]):
        address_data['apartment'] = -1
        address = Address(**address_data)
        with pytest.raises(ValidationError):
            address.full_clean()
