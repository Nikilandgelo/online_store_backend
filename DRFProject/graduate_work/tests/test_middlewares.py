import pytest
from User.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.mark.django_db
class TestEmailConfirmationMiddleware:

    @pytest.fixture
    def create_users(self):
        user_confirmed = User.objects.create(
            username='confirmeduser',
            email='confirmed@example.com',
            password='password123',
            is_email_confirm=True
        )
        user_unconfirmed = User.objects.create(
            username='unconfirmeduser',
            email='unconfirmed@example.com',
            password='password123'
        )
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        return user_confirmed, user_unconfirmed, superuser

    @pytest.fixture
    def get_tokens(self, create_users: tuple[User, User, User]) -> tuple:
        user_confirmed, user_unconfirmed, superuser = create_users
        return (Token.objects.get(user=user_confirmed).key,
                Token.objects.get(user=user_unconfirmed).key,
                Token.objects.get(user=superuser).key)

    @pytest.fixture
    def client(self) -> APIClient:
        return APIClient()

    def test_no_token(self):
        response = APIClient().post(reverse('registration_user'), data={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'supersecretpassword'
            })
        assert response.status_code != 400

    def test_invalid_token(self, client: APIClient):
        client.credentials(HTTP_AUTHORIZATION='Token invalidtoken')
        response = client.post(reverse('categories-list'),
                               data={'name': 'category'})
        assert response.status_code == 400
        assert response.content.decode() == 'Invalid token'

    def test_unconfirmed_email(self, client: APIClient, get_tokens):
        _, token_unconfirmed, _ = get_tokens
        client.credentials(HTTP_AUTHORIZATION=f'Token {token_unconfirmed}')
        response = client.post(reverse('shops-list'),
                               data={'name': 'shop',
                                     'categories': ['category'],
                                     'owners': []})
        assert response.status_code == 400
        assert response.content.decode() == 'Your email is not confirmed'

    def test_confirmed_email(self, client: APIClient, get_tokens):
        token_confirmed, _, _ = get_tokens
        client.credentials(HTTP_AUTHORIZATION=f'Token {token_confirmed}')
        response = client.post(reverse('shops-list'),
                               data={'name': 'shop',
                                     'categories': ['category'],
                                     'owners': []})
        assert response.content.decode() != 'Your email is not confirmed'

    def test_superuser(self, client: APIClient, get_tokens):
        _, _, token_superuser = get_tokens
        client.credentials(HTTP_AUTHORIZATION=f'Token {token_superuser}')
        response = client.post(reverse('categories-list'),
                               data={'name': 'category'})
        assert response.status_code != 400
