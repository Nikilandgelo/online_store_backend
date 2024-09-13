from rest_framework.views import APIView
from ShoppingCart.models import ShoppingCartProducts
from ShoppingCart.serializers import (
    ShoppingCartSerializer, GetShoppingCartSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction


class ShoppingCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_shopping_products = ShoppingCartProducts.objects.filter(
            shopping_cart=request.user.shopping_cart.first()
        ).select_related('product')

        serializer = GetShoppingCartSerializer(
            all_shopping_products, many=True)
        return Response(serializer.data, 200)

    def post(self, request):
        serializer = ShoppingCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(shopping_cart=request.user.shopping_cart.first())
        return Response('Product has been added to shopping cart', 201)

    def delete(self, request):
        all_shopping_products = ShoppingCartProducts.objects.filter(
            shopping_cart=request.user.shopping_cart.first()
        )
        products_for_delete: list = request.data.get('products')
        if not isinstance(products_for_delete, list):
            return Response('Product ids must be a list', 400)
        if not all(isinstance(id_product, int)
                   for id_product in products_for_delete):
            return Response('All ids must be integers', 400)
        try:
            with transaction.atomic():
                for id_product in products_for_delete:
                    all_shopping_products.get(product__id=id_product).delete()
        except ShoppingCartProducts.DoesNotExist:
            return Response(
                (f'Product with id {id_product} in your shopping cart'
                 f' does not exists'), 400)

        return Response('Products have been deleted', 204)
