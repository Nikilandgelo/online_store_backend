from django.db import models


class Category(models.Model):
    """
    Model to represent a category of products.

    Attributes:
        name (str): The name of the category.
    """
    name = models.CharField(max_length=255, unique=True)

    # ALL RELATED FIELDS
    # - shops

    def __str__(self):
        return self.name
