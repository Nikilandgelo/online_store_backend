from django.db import models
from Product.models import Product


class Parameter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='parameters')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ['product', 'name']
