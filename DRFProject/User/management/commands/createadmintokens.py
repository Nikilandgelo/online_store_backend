from django.core.management.base import BaseCommand
from django.db.models import Q
from User.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    """
    This custom management command creates tokens for all admin users that
    don't have one yet.
    """
    def handle(self, *args, **options):
        for admin in User.objects.filter(
                Q(is_superuser=True) | Q(is_staff=True)):
            try:
                Token.objects.get(user=admin)
            except Token.DoesNotExist:
                Token.objects.create(user=admin)
