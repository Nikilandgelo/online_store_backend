import pytest
from User.models import User
from Adress.serializers import AdressSerializer
from Adress.models import Address


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
def address_data(user: User) -> dict[str, any]:
    return {
        "user": user,
        "city": "Test City",
        "street": "Test Street",
        "house_number": 123,
        "hull_building": "A",
        "apartment": 10,
    }


@pytest.mark.django_db
class TestAdressSerializer:

    def test_valid_address_serialization(self, address_data: dict[str, any]):
        serializer = AdressSerializer(data=address_data)
        assert serializer.is_valid()
        serialized_data = serializer.validated_data

        assert serialized_data['city'] == address_data['city']
        assert serialized_data['street'] == address_data['street']
        assert serialized_data['house_number'] == address_data['house_number']
        assert serialized_data['hull_building'] == address_data[
            'hull_building']
        assert serialized_data['apartment'] == address_data['apartment']

    def test_invalid_city_name(self, address_data: dict[str, any]):
        address_data['city'] = ""
        serializer = AdressSerializer(data=address_data)

        assert not serializer.is_valid()
        assert 'city' in serializer.errors

    def test_partial_update_address(self, address_data: dict[str, any]):
        address: Address = Address.objects.create(**address_data)
        serializer = AdressSerializer(address, data={"city": "Updated City"},
                                      partial=True)
        assert serializer.is_valid()
        updated_address = serializer.save()

        assert updated_address.city == "Updated City"
        assert updated_address.street == address_data['street']
        assert updated_address.house_number == address_data['house_number']

    def test_invalid_house_number(self, address_data: dict[str, any]):
        address_data['house_number'] = -1
        serializer = AdressSerializer(data=address_data)

        assert not serializer.is_valid()
        assert 'house_number' in serializer.errors
