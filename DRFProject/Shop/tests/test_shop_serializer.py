import pytest
from User.models import User
from Categories.models import Category
from Shop.models import Shop, ShopCategories, ShopOwners
from Shop.serializers import ShopSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ValidationError


@pytest.fixture
def category() -> Category:
    return Category.objects.create(name="Electronics")


@pytest.fixture
def another_category() -> Category:
    return Category.objects.create(name="Books")


@pytest.fixture
def user() -> User:
    return User.objects.create(
        first_name="Test",
        last_name="User",
        username="testuser",
        email="testuser@example.com",
        password="password123")


@pytest.fixture
def another_user() -> User:
    return User.objects.create(
        first_name="Another",
        last_name="User",
        username="anotheruser",
        email="anotheruser@example.com",
        password="password123")


@pytest.fixture
def shop() -> Shop:
    return Shop.objects.create(name="Test Shop", is_accepting_orders=True)


@pytest.mark.django_db
class TestShopSerializer:

    def test_shop_serializer_valid_data(self, category: Category,
                                        user: User):
        data = {
            "name": "New Shop",
            "categories": [category.name],
            "owners": [user.email]
        }
        serializer = ShopSerializer(data=data)
        assert serializer.is_valid()
        validated_data = serializer.validated_data
        assert validated_data['name'] == "New Shop"

    def test_shop_serializer_invalid_empty_categories(self, user: User):
        data = {
            "name": "New Shop",
            "categories": [],
            "owners": [user.email]
        }
        serializer = ShopSerializer(data=data)
        assert not serializer.is_valid()
        assert 'Categories cannot be empty' in str(
            serializer.errors['categories'])

    def test_create_shop_valid(self, category: Category, user: User,
                               another_user: User):
        data = {
            "name": "Valid Shop",
            "categories": [category.name],
            "owners": [another_user.email]
        }
        request = APIRequestFactory().get('')
        request.user = user
        context = {'request': request}
        serializer = ShopSerializer(data=data, context=context)

        assert serializer.is_valid()
        shop = serializer.create(serializer.validated_data)
        assert shop.name == "Valid Shop"
        assert shop.is_accepting_orders is True
        assert ShopCategories.objects.filter(
            shop=shop, category=category).exists()
        assert ShopOwners.objects.filter(
            shop=shop, owner=user).exists()
        assert ShopOwners.objects.filter(
            shop=shop, owner=another_user).exists()

    def test_invalid_create_shop_duplicate_owner(
            self, category: Category, user: User, another_user: User):
        data = {
            "name": "Invalid Shop",
            "categories": [category.name],
            "owners": [user.email, another_user.email]
        }
        request = APIRequestFactory().get('')
        request.user = user
        context = {'request': request}
        serializer = ShopSerializer(data=data, context=context)

        assert serializer.is_valid()
        with pytest.raises(ValidationError) as exc_info:
            serializer.create(serializer.validated_data)
        assert 'duplicate key' in str(exc_info.value)

    def test_update_shop(self, shop: Shop, category: Category, user: User,
                         another_user: User):
        data = {
            "name": "Updated Shop Name",
            "categories": [category.name],
            "owners": [another_user.email],
            "is_accepting_orders": False
        }
        request = APIRequestFactory().put('')
        request.user = user
        context = {'request': request}
        serializer = ShopSerializer(data=data, context=context)

        assert serializer.is_valid()
        updated_shop = serializer.update(
            instance=shop, validated_data=serializer.validated_data)

        assert updated_shop.name == "Updated Shop Name"
        assert updated_shop.is_accepting_orders is False
        assert ShopCategories.objects.filter(
            shop=updated_shop, category=category).exists()
        assert ShopOwners.objects.filter(
            shop=updated_shop, owner=another_user).exists()

    def test_create_shop_integrity_error(self, category: Category,
                                         user: User, shop: Shop):
        # same name
        data = {
            "name": "Test Shop",
            "categories": [category.name],
            "owners": []
        }
        request = APIRequestFactory().post('')
        request.user = user
        context = {'request': request}
        serializer = ShopSerializer(data=data, context=context)

        assert serializer.is_valid() is False
