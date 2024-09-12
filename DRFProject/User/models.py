from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    # Override the default user model fields, 70 value because:
    # username max length is 150 and username has pattern f.e.:
    # first_name-last_name_1. So with the current constraint 70 we can hold up
    # users to first_name-last_name_99999999 with equal full names.
    first_name = models.CharField(max_length=70, verbose_name='first name')
    last_name = models.CharField(max_length=70, verbose_name='last name')
    email = models.EmailField(unique=True, verbose_name='email address')
    is_email_confirm = models.BooleanField(default=False)

    # ALL RELATED FIELDS
    # - shops
    # - addresses
    # - shopping_cart
    # - orders
    # - auth_token

    def save(self, *args, **kwargs) -> None:
        """
        Convert the email to lower case to keep consistency with the email
        in the database. This is necessary because the email uniqueness
        constraint is case sensitive and if the email is not converted to lower
        case, it could lead to users with the same email but different cases.
        """
        self.email: str = self.email.lower()
        super().save(*args, **kwargs)
