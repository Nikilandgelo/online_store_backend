from rest_framework.views import APIView
from rest_framework.response import Response
from Order.serializers import (
    OrderSerializer, GetOrderSerializer, ChangeStatusSerializer)
from rest_framework.permissions import IsAuthenticated
from Order.models import Order
from rest_framework.decorators import api_view
from rest_framework.request import Request
from User.tasks import send_email
from django.shortcuts import get_object_or_404
from graduate_work.html_forms import EMAIL_FOR_ADMIN


class ListOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = GetOrderSerializer(orders, many=True)
        return Response(serializer.data, 200)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response('Order has been created', 201)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order: Order = get_object_or_404(Order, id=pk)
        if order.user != request.user:
            return Response('You can`t see not your order', 400)
        serializer = GetOrderSerializer(order)
        return Response(serializer.data, 200)

    def patch(self, request, pk):
        if not request.user.is_superuser:
            return Response('This action is not allowed', 400)
        order: Order = get_object_or_404(Order, id=pk)
        serializer = ChangeStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(order, serializer.validated_data)
        return Response('Order status has been updated', 200)

    def delete(self, request, pk):
        if not request.user.is_superuser:
            return Response('This action is not allowed', 400)
        order: Order = get_object_or_404(Order, id=pk)
        order.delete()
        return Response('Order has been deleted', 200)


@api_view(['GET'])
def confirm_order(request: Request, pk: int):
    order: Order = get_object_or_404(Order, id=pk)
    if order.user.auth_token.key != request.query_params.get('token'):
        return Response('You can`t confirm not your order', 400)
    if order.status != Order.Status.CREATED:
        return Response('Order already confirmed', 400)
    order.status = Order.Status.CONFIRMED
    order.save()
    user_order: str = ''.join(
        map(lambda order_products: (
            f'<li>Product ID - {order_products.product.id},<br>'
            f'Product name - {order_products.product.name},<br>'
            f'Quantity - {order_products.quantity}</li><br>'),
            order.order_products.all())
        )
    send_email.delay(title='New order',
                     html_message=EMAIL_FOR_ADMIN.format(
                         user=order.user.username, user_order=user_order,
                         overall_price=order.total_price),
                     mail_for_admin=True)
    return Response('Order has been confirmed', 200)
