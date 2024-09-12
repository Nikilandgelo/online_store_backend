from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from Shop.models import ShopCategories
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes: list = [IsAdminUser]

    def get_permissions(self):
        """
        Get the permissions for the current request.

        Overrides the default implementation to allow all safe methods
        and to return the permissions defined in the superclass
        for all other methods.

        Returns:
            A list of permission classes.
        """
        if self.request.method in SAFE_METHODS:
            return []
        else:
            return super().get_permissions()

    @action(methods=['DELETE'], detail=True, url_path='remove-shops',
            url_name='remove_shops')
    def remove_objects(self, request, pk):
        """
        Custom action to remove shops from a category.
        """
        try:
            with transaction.atomic():
                shops_for_delete = request.data['shops']
                if not isinstance(shops_for_delete, list):
                    raise ValueError
                for shop_id in shops_for_delete:
                    if not isinstance(shop_id, int):
                        raise TypeError
                    get_object_or_404(
                        ShopCategories, category=pk, shop=shop_id).delete()
        except (KeyError, ValueError):
            return Response(
                'You must provide field "shops" with a list of shop ids',
                status=400)
        except TypeError:
            return Response('Invalid type of shop id', status=400)

        return Response('Shops have been removed', 200)
