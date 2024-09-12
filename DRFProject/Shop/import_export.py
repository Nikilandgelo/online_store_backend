from rest_framework.decorators import action
from .models import Shop
from rest_framework.parsers import JSONParser
from rest_framework_yaml.parsers import YAMLParser
from rest_framework.response import Response
from Product.serializers import ProductSerializer
from django.db.utils import IntegrityError
from django.db import transaction
from django.shortcuts import get_object_or_404
from Shop.serializers import ShopProductsOrders
from django.db.models import Count
from django.http import StreamingHttpResponse
import json


def import_wrapper(url_path: str):
    """
    Returns a function to import products in the format of a dictionary
    where the keys are the names of the products and the values are
    dictionaries containing the description, parameters, quantity, and price
    of the product.
    """
    @action(detail=True, methods=['POST'], url_path=url_path,
            url_name='import', parser_classes=[JSONParser, YAMLParser])
    def import_products(self, request, pk):
        """
        Imports products into the shop with the given pk.
        """
        shop: Shop = get_object_or_404(Shop, id=pk)
        if request.user not in shop.owners.all():
            return Response('This action is forbidden', status=403)

        if not isinstance(request.data, dict) or not request.data:
            return Response(
                ('Invalid data structure: Expected a non-empty dictionary '
                 'of products.'), status=400)

        try:
            with transaction.atomic():
                for name, other_params in request.data.items():
                    if not isinstance(other_params, dict):
                        raise IntegrityError(
                            f'Invalid structure for product {name}')
                    if set(other_params) != {
                            'description', 'quantity', 'price', 'parameters'}:
                        raise IntegrityError(
                            (f'Invalid product with name {name}, your product '
                             'must have "description", "quantity", "price" and'
                             ' "parameters" fields.'))

                    other_params['name'] = name
                    serializer = ProductSerializer(data=other_params)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(shop=shop)
        except IntegrityError as error:
            return Response(str(error), 400)
        return Response('Your products have been imported', status=200)

    return import_products


def export_wrapper(url_path: str):
    """
    Returns a function to export products in the format of a JSON array
    where each element is a dictionary containing the order id, product name,
    product quantity, and product price.
    """
    @action(detail=True, methods=['GET'], url_path=url_path, url_name='export')
    def export_products(self, request, pk):
        """
        Exports products of the shop with the given pk.

        Returns:
            StreamingHttpResponse: A StreamingHttpResponse containing the
            products in JSON format.
        """
        shop: Shop = get_object_or_404(Shop, id=pk)
        if request.user not in shop.owners.all():
            return Response('This action is forbidden', status=403)
        seen_orders = set()

        def generate_orders_products():
            yield '[\n\t'
            first_item = True
            for product in shop.products.annotate(
                    orders_count=Count('orders')).filter(orders_count__gt=0):
                for order in product.orders.all():
                    if order.order not in seen_orders:
                        seen_orders.add(order.order)
                        if not first_item:
                            yield ',\n\t'
                        else:
                            first_item = False
                        yield json.dumps(ShopProductsOrders(order).data,
                                         ensure_ascii=False, indent=6)
            yield '\n]'
        response = StreamingHttpResponse(generate_orders_products(),
                                         content_type='application/json')
        response['Content-Disposition'] = (
            f'attachment; filename="{shop.name}_orders.json"')
        return response

    return export_products
