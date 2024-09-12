import pytest
from rest_framework.serializers import ValidationError
from Categories.serializers import CategorySerializer
from Categories.models import Category
from Shop.models import Shop, ShopCategories
from model_bakery import baker


@pytest.fixture
def create_shop():
    def wrapper(name: str, category: Category):
        shop: Shop = baker.make(Shop, name=name)
        baker.make(ShopCategories, shop=shop, category=category)
        return shop
    return wrapper


@pytest.mark.django_db
class TestCategorySerializer:

    def test_category_serializer_valid_data(self):
        """
        Test the CategorySerializer with valid data.
        """
        category: Category = Category.objects.create(name="Electronics")
        serializer = CategorySerializer(category)
        expected_data = {
            'name': 'Electronics',
            'shops': []
        }
        assert serializer.data == expected_data

    def test_category_serializer_with_related_shops(self, create_shop):
        """
        Test CategorySerializer when the category has related shops.
        """
        category: Category = Category.objects.create(name="Groceries")
        create_shop(name="SuperMart", category=category)
        create_shop(name="GreenGrocer", category=category)

        serializer = CategorySerializer(category)
        expected_data = {
            'name': 'Groceries',
            'shops': ['SuperMart', 'GreenGrocer']
        }
        assert serializer.data == expected_data

    def test_category_serializer_missing_required_field(self):
        """
        Test that serializer raises ValidationError when required fields are
        missing.
        """
        invalid_data = {'shops': []}
        serializer = CategorySerializer(data=invalid_data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_category_serializer_invalid_data(self):
        """
        Test CategorySerializer with invalid data.
        """
        invalid_data = {
            'name': '',
            'shops': []
        }
        serializer = CategorySerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors
