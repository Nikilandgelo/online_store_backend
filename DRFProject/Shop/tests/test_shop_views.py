import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from Shop.models import Shop, ShopCategories, ShopOwners
from User.models import User
from Categories.models import Category


@pytest.fixture
def category() -> Category:
    return Category.objects.create(name="Electronics")


@pytest.fixture
def user() -> User:
    return User.objects.create(
        first_name="Test",
        last_name="User",
        username="testuser",
        email="testuser@example.com",
        password="password123",
        is_email_confirm=True)


@pytest.fixture
def another_user() -> User:
    return User.objects.create(
        first_name="Another",
        last_name="User",
        username="anotheruser",
        email="anotheruser@example.com",
        password="password123")


@pytest.fixture
def shop(category: Category, user: User) -> Shop:
    shop: Shop = Shop.objects.create(
        name="Test Shop", is_accepting_orders=True)
    ShopCategories.objects.create(shop=shop, category=category)
    ShopOwners.objects.create(shop=shop, owner=user)
    return shop


@pytest.fixture
def shop_owner(user: User) -> APIClient:
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token}')
    return client


@pytest.mark.django_db
def test_list_shops(shop: Shop, category: Category):
    response = APIClient().get(reverse('shops-list'))

    assert response.status_code == 200
    assert len(response.data) > 0
    assert response.data[0]['name'] == shop.name
    assert response.data[0]['is_accepting_orders'] is True
    assert response.data[0]['categories'][0] == category.id


@pytest.mark.django_db
def test_create_shop(shop_owner: APIClient, user: User, category: Category):
    data = {
        "name": "New Shop",
        "categories": [category.name],
        "owners": []
    }
    response = shop_owner.post(reverse('shops-list'), data=data)

    assert response.status_code == 201
    assert response.data['name'] == "New Shop"
    assert Shop.objects.filter(name="New Shop").exists()
    assert ShopCategories.objects.filter(
        shop__name="New Shop", category=category).exists()
    assert ShopOwners.objects.filter(
        shop__name="New Shop", owner=user).exists()


@pytest.mark.django_db
def test_update_shop(shop_owner: APIClient, shop: Shop, category: Category,
                     another_user: User):
    data = {
        "name": "Updated Shop",
        "categories": [category.name],
        "owners": [another_user.email],
        "is_accepting_orders": False
    }
    response = shop_owner.put(reverse('shops-detail', args=[shop.id]), data)

    assert response.status_code == 200
    assert response.data['name'] == "Updated Shop"
    assert response.data['is_accepting_orders'] is False
    assert ShopOwners.objects.filter(shop=shop, owner=another_user).exists()


@pytest.mark.django_db
def test_delete_shop(shop_owner: APIClient, shop: Shop):
    response = shop_owner.delete(reverse('shops-detail', args=[shop.id]))

    assert response.status_code == 204
    assert not Shop.objects.filter(id=shop.id).exists()


@pytest.mark.django_db
def test_import_products(shop_owner: APIClient, shop: Shop):
    data = {
        "Product 1": {
            "description": "Test product",
            "quantity": 10,
            "price": 100,
            "parameters": [
                {
                    "name": "Color",
                    "value": "Red"
                }
            ]
        }
    }
    response = shop_owner.post(reverse('shops-import',
                                       args=[shop.id]), data)
    assert response.status_code == 200
    assert 'Your products have been imported' in response.data


@pytest.mark.django_db
def test_import_products_invalid_data(shop_owner: APIClient, shop: Shop):
    invalid_data = ["Invalid Product Structure"]

    response = shop_owner.post(
        reverse('shops-import', args=[shop.id]), invalid_data)

    assert response.status_code == 400
    assert 'Invalid data structure' in response.data


@pytest.mark.django_db
def test_export_products(shop_owner: APIClient, shop: Shop):
    response = shop_owner.get(
        reverse('shops-export', args=[shop.id]))

    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'
    assert response['Content-Disposition'].startswith(
        f'attachment; filename="{shop.name}_orders.json"')


@pytest.mark.django_db
def test_create_shop_unauthenticated(category):
    data = {
        "name": "New Shop",
        "categories": [category.name],
        "owners": ["nonexistent@example.com"]
    }
    response = APIClient().post(reverse('shops-list'), data)
    assert response.status_code == 401
