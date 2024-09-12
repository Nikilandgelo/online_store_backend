from rest_framework.serializers import (
    Serializer, ModelSerializer, ValidationError)
from .models import ShoppingCartProducts
from django.db import transaction, IntegrityError
from Product.serializers import ProductSerializer


class GetShoppingCartSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ShoppingCartProducts
        fields = ['product', 'quantity']


class ShoppingCartProductsSerializer(ModelSerializer):

    class Meta:
        model = ShoppingCartProducts
        fields = ['product', 'quantity']


class ShoppingCartSerializer(Serializer):
    products = ShoppingCartProductsSerializer(many=True)

    def validate_products(self, value):
        if len(value) == 0:
            raise ValidationError("You must to pass at least one product")
        return value

    def create(self, validated_data: dict):
        shopping_cart = validated_data.pop('shopping_cart')
        try:
            with transaction.atomic():
                for product in validated_data.pop('products'):
                    product['shopping_cart'] = shopping_cart
                    quantity = product.get('quantity') or 1
                    if quantity > product['product'].quantity:
                        raise IntegrityError(
                            (f'Quantity is too big, you can only buy'
                             f'{product["product"].quantity} products'))
                    ShoppingCartProducts.objects.create(**product)
        except IntegrityError as error:
            raise ValidationError(str(error)) from error
        return shopping_cart
