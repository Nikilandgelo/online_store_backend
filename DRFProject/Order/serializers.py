from rest_framework.serializers import (
    ModelSerializer, ValidationError, StringRelatedField,
    Serializer, ChoiceField)
from .models import Order, OrderProducts
from django.db import transaction, IntegrityError
from ShoppingCart.models import ShoppingCartProducts
from User.models import User
from Product.models import Product
from User.tasks import send_email
import os
from graduate_work.html_forms import EMAIL_CONFIRM_ORDER
from django.urls import reverse


class GetOrderProductsSerializer(ModelSerializer):
    product = StringRelatedField()

    class Meta:
        model = OrderProducts
        fields = ['product', 'quantity']


class GetOrderSerializer(ModelSerializer):
    user = StringRelatedField()
    address = StringRelatedField()
    order_products = GetOrderProductsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'address', 'status', 'created', 'updated',
                  'total_price', 'order_products']


class OrderSerializer(ModelSerializer):

    class Meta:
        model = Order
        fields = ['address']

    def create(self, validated_data: dict):
        user: User = validated_data.get('user')
        if validated_data.get('address') not in user.addresses.all():
            raise ValidationError(
                'This address is not yours, please pass the correct address.')
        try:
            with transaction.atomic():
                order: Order = Order.objects.create(**validated_data)
                total_price = 0
                for shopping_product in ShoppingCartProducts.objects.filter(
                        shopping_cart=user.shopping_cart.first()):
                    product: Product = shopping_product.product
                    if not product.shop.is_accepting_orders:
                        raise ValidationError(
                            ('Sorry, the shop owners of this product '
                             f'"{product.name}" are not accepting orders '
                             'right now. Please remove it from your shopping '
                             'cart or try again later.'))

                    quantity: int = shopping_product.quantity
                    total_price += product.price * quantity
                    product.quantity -= quantity
                    product.save()
                    shopping_product.delete()
                    OrderProducts.objects.create(order=order, product=product,
                                                 quantity=quantity)
                if total_price <= 0:
                    raise ValidationError('Your shopping cart is empty')
                order.total_price = total_price
                order.save()
        except IntegrityError as error:
            raise ValidationError(
                (f'Sorry, product "{product.name}" is temporarily not'
                 ' available in the desired quantity.')) from error
        send_email.delay(title='Confirm your order',
                         email=user.email,
                         html_message=EMAIL_CONFIRM_ORDER.format(
                             url=(f'{os.getenv("SERVER_SOCKET")}'
                                  + reverse("confirm_order", kwargs={
                                      "pk": order.id})
                                  + f'?token={user.auth_token.key}'
                                  ))
                         )
        return order


class ChangeStatusSerializer(Serializer):
    status = ChoiceField(choices=Order.Status.choices, required=True)

    def update(self, instance: Order, validated_data: dict):
        instance.status = validated_data.get('status')
        instance.save()
        return instance
