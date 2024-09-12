from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from User.views import (RegistrationView, login,
                        ResetPasswordView, change_password)
from Shop.views import ShopViewSet
from Categories.views import CategoryViewSet
from Product.views import ProductView, ProductDetailView
from Adress.views import AdressView
from ShoppingCart.views import ShoppingCartView
from Order.views import ListOrdersView, OrderView, confirm_order


router = routers.SimpleRouter()
router.register('shops', ShopViewSet, basename='shops')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns: list = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('users/', RegistrationView.as_view(), name='registration_user'),
    path('users/login/', login, name='login_user'),
    path('users/add-address/', AdressView.as_view(), name='add_address'),
    path('users/reset-password/', ResetPasswordView.as_view(),
         name='ask_reset_password'),
    path('users/change-pw/', change_password, name='change_password'),
    path('products/', ProductView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('shopping-cart/', ShoppingCartView.as_view()),
    path('orders/', ListOrdersView.as_view(), name='list_orders'),
    path('orders/<int:pk>/', OrderView.as_view(), name='order'),
    path('orders/<int:pk>/confirm/', confirm_order, name='confirm_order'),
]
