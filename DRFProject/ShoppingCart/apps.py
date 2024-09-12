from django.apps import AppConfig


class ShoppingcartConfig(AppConfig):
    name = 'ShoppingCart'

    def ready(self):
        import ShoppingCart.signals
