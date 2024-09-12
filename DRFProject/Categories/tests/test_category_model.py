import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from Categories.models import Category


@pytest.mark.django_db
class TestCategoryModel:

    def test_create_category(self):
        category = Category.objects.create(name="Electronics")
        assert category.name == "Electronics"
        assert str(category) == "Electronics"

    def test_category_name_uniqueness(self):
        Category.objects.create(name="Electronics")
        with pytest.raises(IntegrityError):
            Category.objects.create(name="Electronics")

    def test_category_max_length_exceeded(self):
        with pytest.raises(ValidationError):
            long_name = "a" * 256
            category = Category(name=long_name)
            category.full_clean()

    def test_blank_name_field(self):
        with pytest.raises(ValidationError):
            category = Category(name="")
            category.full_clean()

    def test_category_str_method(self):
        category: Category = Category.objects.create(name="Books")
        assert str(category) == "Books"
