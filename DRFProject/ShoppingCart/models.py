from django.db import models
from User.models import User
from Product.models import Product


class ShoppingCartProducts(models.Model):
    shopping_cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='shopping_carts')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['shopping_cart', 'product']


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_cart')
    products = models.ManyToManyField(Product, through='ShoppingCartProducts')
