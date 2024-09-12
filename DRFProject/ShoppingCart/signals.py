from django.db.models.signals import post_save
from django.dispatch import receiver
from User.models import User
from rest_framework.authtoken.models import Token
from ShoppingCart.models import ShoppingCart
from User.tasks import send_email
import os
from graduate_work.html_forms import EMAIL_CONFIRM_EMAIL
from django.urls import reverse
from django.db import transaction, IntegrityError


@receiver(post_save, sender=User)
def create_user_related_objects(sender: User, instance: User,
                                created: bool, **kwargs):
    """
    Creates related objects for a user instance.

    This receiver is triggered when a new user is created.
    It will create a token for the user and a ShoppingCart instance for
    the user to hold their cart items. It will also send a confirmation email
    to the user with a link to confirm their email address.
    """
    if created:
        try:
            with transaction.atomic():
                token: Token = Token.objects.create(user=instance)
                ShoppingCart.objects.create(user=instance)
                url: str = (f'{os.getenv("SERVER_SOCKET")}'
                            f'{reverse("registration_user")}'
                            f'?token={token.key}')
                send_email.delay(title='Confirm your email address',
                                 email=instance.email,
                                 html_message=EMAIL_CONFIRM_EMAIL.format(
                                     url=url))
        except IntegrityError:
            print('SOMETHING WENT WRONG WITH CREATING USER RELATED OBJECTS!!!')
