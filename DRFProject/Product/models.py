from django.db import models
from Shop.models import Shop


class Product(models.Model):
    name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,
                             related_name='products')
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    description = models.TextField()

    # ALL RELATED FIELDS
    # - parameters
    # - shopping_carts
    # - orders

    class Meta:
        unique_together = ['name', 'shop']

    def __str__(self) -> str:
        return self.name
