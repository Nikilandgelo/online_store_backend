from rest_framework import viewsets
from .models import Shop
from .serializers import ShopSerializer
from graduate_work.permissions import IsOwnerOrReadOnlyOrAdmin
from rest_framework.permissions import IsAuthenticated
from .import_export import import_wrapper, export_wrapper
from .filters import ShopFilterSet


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes: list = [IsOwnerOrReadOnlyOrAdmin(['owners'])]
    filterset_class = ShopFilterSet

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return super().get_permissions()

    import_products = import_wrapper('import-products')
    export_products = export_wrapper('export-ordered-products')
