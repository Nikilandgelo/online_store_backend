from django.db import models
from User.models import User
from Adress.models import Address
from Product.models import Product


class Order(models.Model):

    class Status(models.TextChoices):
        CREATED = "Создан"
        CONFIRMED = "Подтвержден"
        IN_PROGRESS = "В пути"
        DELIVERED = "Доставлен"

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE,
                                related_name='orders')
    status = models.CharField(max_length=15, choices=Status.choices,
                              default=Status.CREATED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_price = models.PositiveIntegerField(default=0)
    products = models.ManyToManyField(Product, through='OrderProducts')


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='orders')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order', 'product')
