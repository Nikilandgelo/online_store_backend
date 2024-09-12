import pytest
from User.models import User
from Order.models import Order, OrderProducts
from Adress.models import Address
from ShoppingCart.models import ShoppingCartProducts
from rest_framework.authtoken.models import Token
from model_bakery.baker import make
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def user():
    return make(User, is_email_confirm=True)


@pytest.fixture
def admin():
    return make(User, is_superuser=True, is_staff=True)


@pytest.fixture
def address(user):
    return make(Address, user=user)


@pytest.fixture
def token(user):
    return Token.objects.get(user=user)


@pytest.fixture
def create_shopping_cart_products(user):
    return make(ShoppingCartProducts, shopping_cart=user.shopping_cart.first())


@pytest.fixture
def order(user):
    return make(Order, user=user)


@pytest.fixture
def confirmed_order(user):
    return make(Order, user=user, status=Order.Status.CONFIRMED)


@pytest.fixture
def order_products(order):
    return make(OrderProducts, order=order, _quantity=2)


@pytest.fixture
def api_client(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.mark.django_db
def test_list_orders_view_get(user, api_client: APIClient, order):
    response = api_client.get(reverse("list_orders"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_list_orders_view_post(address: Address, api_client: APIClient,
                               create_shopping_cart_products):
    data = {"address": address.id}
    response = api_client.post(reverse("list_orders"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.count() == 1


@pytest.mark.django_db
def test_list_orders_view_post_invalid_data(
        api_client: APIClient, create_shopping_cart_products: APIClient):
    data = {"invalid_field": "Invalid Data"}
    response = api_client.post(reverse("list_orders"), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_order_view_get(api_client: APIClient, order):
    response = api_client.get(reverse("order", args=[order.id]))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_order_view_patch(admin, order):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {admin.auth_token.key}")

    data = {"status": "Доставлен"}
    response = client.patch(reverse("order", args=[order.id]), data)
    assert response.status_code == status.HTTP_200_OK
    assert Order.objects.get(id=order.id).status == "Доставлен"


@pytest.mark.django_db
def test_order_view_patch_invalid_data(api_client: APIClient, order):
    data = {"invalid_field": "Invalid Data"}
    response = api_client.patch(reverse("order", args=[order.id]), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_order_view_delete(admin, order):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {admin.auth_token.key}")

    response = client.delete(reverse("order", args=[order.id]))
    assert response.status_code == 200
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_confirm_order_valid_token(api_client: APIClient, order, token):
    response = api_client.get(
        reverse("confirm_order", kwargs={"pk": order.id}), {"token": token})
    assert response.status_code == status.HTTP_200_OK
    assert response.data == "Order has been confirmed"
    order.refresh_from_db()
    assert order.status == Order.Status.CONFIRMED


@pytest.mark.django_db
def test_confirm_order_invalid_token(api_client: APIClient, order):
    response = api_client.get(
        reverse("confirm_order", kwargs={"pk": order.id}),
        {"token": 'invalid'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "You can`t confirm not your order"


@pytest.mark.django_db
def test_confirm_order_already_confirmed(api_client, confirmed_order, token):
    response = api_client.get(
        reverse("confirm_order", kwargs={"pk": confirmed_order.id}),
        {"token": token})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "Order already confirmed"


@pytest.mark.django_db
def test_confirm_order_non_existent_order(api_client):
    response = api_client.get(
        reverse("confirm_order", kwargs={"pk": '9999'}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
