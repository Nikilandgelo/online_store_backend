import pytest
from Shop.models import Shop, ShopCategories, ShopOwners
from Categories.models import Category
from User.models import User
from model_bakery import baker
from django.core.exceptions import ValidationError


@pytest.fixture
def user_data() -> dict[str, str]:
    return {
        "username": "shop_owner",
        "first_name": "John",
        "last_name": "Doe",
        "email": "shopowner@example.com",
        "password": "password123"
    }


@pytest.fixture
def user(user_data: dict[str, str]):
    return baker.make(User, **user_data)


@pytest.fixture
def category_data() -> dict[str, str]:
    return {
        "name": "Electronics"
    }


@pytest.fixture
def category(category_data: dict[str, str]):
    return baker.make(Category, **category_data)


@pytest.fixture
def shop_data() -> dict[str, str]:
    return {
        "name": "Tech Store"
    }


@pytest.fixture
def shop(shop_data: dict[str, str]) -> Shop:
    return baker.make(Shop, **shop_data)


@pytest.mark.django_db
class TestShopModel:
    def test_create_shop(self, shop_data: dict[str, str], shop):
        assert shop.name == shop_data.get("name")
        assert str(shop) == shop_data.get("name")
        assert shop.is_accepting_orders is True

    def test_unique_shop_name(self, shop_data: dict[str, str], shop):
        with pytest.raises(Exception):                # IntegrityError expected
            Shop.objects.create(**shop_data)

    def test_shop_without_name(self, shop_data):
        shop_data['name'] = ""
        shop = Shop.objects.create(**shop_data)
        with pytest.raises(ValidationError):
            shop.full_clean()

    def test_add_category_to_shop(self, shop, category):
        shop_category = ShopCategories.objects.create(
            shop=shop, category=category)
        assert shop_category.shop == shop
        assert shop_category.category == category

    def test_add_owner_to_shop(self, shop, user):
        shop_owner = ShopOwners.objects.create(shop=shop, owner=user)
        assert shop_owner.shop == shop
        assert shop_owner.owner == user

    def test_shop_unique_owner(self, shop, user):
        ShopOwners.objects.create(shop=shop, owner=user)
        with pytest.raises(Exception):                # IntegrityError expected
            ShopOwners.objects.create(shop=shop, owner=user)

    def test_shop_unique_category(self, shop, category):

        ShopCategories.objects.create(shop=shop, category=category)
        with pytest.raises(Exception):                # IntegrityError expected
            ShopCategories.objects.create(shop=shop, category=category)

    def test_shop_is_accepting_orders(self, shop: Shop):
        assert shop.is_accepting_orders is True

        shop.is_accepting_orders = False
        shop.save()
        updated_shop = Shop.objects.get(id=shop.id)
        assert updated_shop.is_accepting_orders is False

    def test_shop_deletion(self, shop: Shop):
        shop_id = shop.id
        shop.delete()

        with pytest.raises(Shop.DoesNotExist):
            Shop.objects.get(id=shop_id)
