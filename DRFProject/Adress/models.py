from django.db import models
from User.models import User


class Address(models.Model):
    """
    Model to represent an address of a user.

    Attributes:
        user (ForeignKey): The user the address belongs to.
        city (CharField): The city of the address.
        street (CharField): The street of the address.
        house_number (PositiveIntegerField): The house number of the address.
        hull_building (CharField): The hull building of the address (optional).
        apartment (PositiveIntegerField): The apartment of the address.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='addresses')
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.PositiveIntegerField()
    hull_building = models.CharField(max_length=50, blank=True, null=True)
    apartment = models.PositiveIntegerField()

    # ALL RELATED FIELDS
    # - orders

    class Meta:
        unique_together: list[str] = ['user', 'city', 'street', 'house_number',
                                      'apartment']

    def __str__(self) -> str:
        return (f'{self.city}, {self.street}, {self.house_number},'
                f'{self.hull_building}, {self.apartment}')
