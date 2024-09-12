import pytest
from User.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from Adress.models import Address
from django.urls import reverse


@pytest.fixture
def user() -> tuple[User, Token]:
    user: User = User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="password123",
        first_name="John",
        last_name="Doe",
        is_email_confirm=True
    )
    return user, Token.objects.get(user=user)


@pytest.fixture
def api_client(user: tuple[User, Token]) -> APIClient:
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {user[1].key}')
    return client


@pytest.fixture
def address_data() -> dict[str, any]:
    return {
        "city": "Test City",
        "street": "Test Street",
        "house_number": 123,
        "hull_building": "A",
        "apartment": 10,
    }


@pytest.fixture
def create_addresses(user: tuple[User, Token]):
    addresses: list[Address] = [Address.objects.create(
        user=user[0],
        city=f"City {i}",
        street=f"Street {i}",
        house_number=i + 1,
        hull_building="",
        apartment=i + 1,
    ) for i in range(5)]
    return addresses


@pytest.mark.django_db
class TestAdressView:

    def test_create_address_successfully(self, api_client: APIClient,
                                         address_data: dict[str, any]):
        response = api_client.post(reverse('add_address'), data=address_data)

        assert response.status_code == 200
        assert response.data == 'Adress has been created'
        assert Address.objects.count() == 1
        address = Address.objects.first()
        assert address.city == address_data['city']

    def test_create_address_limit_exceeded(self, api_client: APIClient,
                                           create_addresses, address_data):
        response = api_client.post(reverse('add_address'), data=address_data)

        assert response.status_code == 400
        assert response.data == 'You can not have more than 5 adresses'
        assert Address.objects.count() == 5

    def test_create_address_with_invalid_data(self, api_client: APIClient,
                                              address_data: dict[str, any]):
        address_data["city"] = ""
        response = api_client.post(reverse('add_address'), data=address_data)

        assert response.status_code == 400
        assert 'city' in response.data
        assert Address.objects.count() == 0

    def test_create_address_with_duplicate_data(self, user: tuple[User, Token],
                                                api_client: APIClient,
                                                address_data: dict[str, any]):
        Address.objects.create(user=user[0], **address_data)
        response = api_client.post(reverse('add_address'), data=address_data)
        assert response.status_code == 400

    def test_unauthenticated_user_cannot_create_address(
            self, address_data: dict[str, any]):
        response = APIClient().post(reverse('add_address'), data=address_data)

        assert response.status_code == 401
        assert Address.objects.count() == 0
