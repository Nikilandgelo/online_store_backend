from django.db import models
from django.contrib.auth import get_user_model
from Categories.models import Category


class Shop(models.Model):
    name = models.CharField(max_length=255, unique=True)
    categories = models.ManyToManyField(Category, through='ShopCategories')
    owners = models.ManyToManyField(get_user_model(), through='ShopOwners')
    is_accepting_orders = models.BooleanField(default=True)

    # ALL RELATED FIELDS
    # - products

    def __str__(self) -> str:
        return self.name


class ShopCategories(models.Model):
    """
    Model to represent the many-to-many relationship between a shop and
    its categories.

    Attributes:
        shop (ForeignKey): The shop.
        category (ForeignKey): The category of the shop.
    """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='shops')

    class Meta:
        unique_together = ['shop', 'category']

    def __str__(self) -> str:
        return self.shop.name


class ShopOwners(models.Model):
    """
    Model to represent the many-to-many relationship between a shop and
    its owners.

    Attributes:
        shop (ForeignKey): The shop.
        owner (ForeignKey): The owner of the shop.
    """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              related_name='shops')

    class Meta:
        unique_together = ['shop', 'owner']
