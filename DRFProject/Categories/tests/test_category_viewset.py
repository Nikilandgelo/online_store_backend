import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from User.models import User
from model_bakery import baker
from Categories.models import Category
from Shop.models import Shop, ShopCategories


@pytest.fixture
def category() -> Category:
    """
    Fixture for creating a Category instance.
    """
    return Category.objects.create(name="Electronics")


@pytest.fixture
def create_shop():
    def wrapper(name: str, category: Category):
        shop: Shop = baker.make(Shop, name=name)
        baker.make(ShopCategories, shop=shop, category=category)
        return shop
    return wrapper


@pytest.fixture
def shop_data(category, create_shop):
    """
    Fixture for creating sample shops related to the category.
    """
    shop1 = create_shop(name="SuperMart", category=category)
    shop2 = create_shop(name="GreenGrocer", category=category)
    return [shop1, shop2]


@pytest.fixture
def admin_user():
    """
    Fixture for creating an admin user.
    """
    return User.objects.create_superuser(
        username="admin", password="adminpass", email="admin@example.com")


@pytest.fixture
def client(admin_user: User) -> APIClient:
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {admin_user.auth_token.key}')
    return client


@pytest.mark.django_db
class TestCategoryViewSet:
    def test_list_categories(self, category: Category):
        """
        Test retrieving a list of categories.
        """
        response = APIClient().get(reverse('categories-list'))
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == category.name

    def test_category_retrieve(self, category):
        """
        Test retrieving a single category by ID.
        """
        response = APIClient().get(
            reverse('categories-detail', args=[category.id]))
        assert response.status_code == 200
        assert response.data["name"] == category.name

    def test_permission_for_non_admin(self):
        """
        Test that non-admin users can't access non-safe methods.
        """
        response = APIClient().post(
            reverse('categories-list'), data={"name": "New Category"})
        assert response.status_code == 401
        assert response.data["detail"] == ("Authentication credentials were"
                                           " not provided.")

    def test_create_category(self, client: APIClient):
        """
        Test creating a new category.
        """
        response = client.post(
            reverse('categories-list'), data={"name": "New Category"})
        assert response.status_code == 201
        assert response.data["name"] == "New Category"

    def test_remove_shops(self, category, shop_data, client: APIClient):
        """
        Test the custom action to remove shops from a category.
        """
        shop_ids = [shop.id for shop in shop_data]
        response = client.delete(
            reverse('categories-remove_shops', args=[category.id]),
            data={"shops": shop_ids})
        assert response.status_code == 200
        assert response.data == "Shops have been removed"

    def test_remove_shops_invalid_data(self, category, shop_data,
                                       client: APIClient):
        """
        Test removing shops with invalid data (non-list for shops).
        """
        response = client.delete(
            reverse('categories-remove_shops', args=[category.id]),
            data={"shops": 123})
        assert response.status_code == 400
        assert response.data == ('You must provide field "shops" with a list'
                                 ' of shop ids')

    def test_remove_shops_invalid_shop_id_type(self, category, shop_data,
                                               client: APIClient):
        """
        Test removing shops with an invalid shop ID type.
        """
        response = client.delete(
            reverse('categories-remove_shops', args=[category.id]),
            data={"shops": ["invalid"]})
        assert response.status_code == 400
        assert response.data == 'Invalid type of shop id'

    def test_remove_shops_nonexistent_shop(self, category, client: APIClient):
        """
        Test removing a non-existent shop from the category.
        """
        response = client.delete(
            reverse('categories-remove_shops', args=[category.id]),
            data={"shops": [978, 646]})
        assert response.status_code == 404
        assert response.data == {'detail':
                                 'No ShopCategories matches the given query.'}

    def test_update_category(self, client: APIClient, category: Category):
        """
        Test updating a category.
        """
        response = client.put(
            reverse('categories-detail', args=[category.id]),
            data={"name": "Updated Category"})
        assert response.status_code == 200
        assert response.data["name"] == "Updated Category"
        category.refresh_from_db()
        assert category.name == "Updated Category"

    def test_delete_category(self, client: APIClient, category: Category):
        """
        Test deleting a category.
        """
        response = client.delete(
            reverse('categories-detail', args=[category.id]))
        assert response.status_code == 204
        assert not Category.objects.filter(id=category.id).exists()

    def test_update_category_permission_for_non_admin(self,
                                                      category: Category):
        """
        Test that non-admin users can't update a category.
        """
        response = APIClient().put(
            reverse('categories-detail', args=[category.id]),
            data={"name": "Updated Category"})
        assert response.status_code == 401
        assert response.data["detail"] == ("Authentication credentials were"
                                           " not provided.")

    def test_delete_category_permission_for_non_admin(self,
                                                      category: Category):
        """
        Test that non-admin users can't delete a category.
        """
        response = APIClient().delete(
            reverse('categories-detail', args=[category.id]))
        assert response.status_code == 401
        assert response.data["detail"] == ("Authentication credentials were"
                                           " not provided.")
