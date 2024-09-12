from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from Product.models import Product
from .serializers import ProductSerializer
from graduate_work.permissions import IsOwnerOrReadOnlyOrAdmin
from .filters import ProductFilterSet


class ProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilterSet


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes: list = [IsOwnerOrReadOnlyOrAdmin(['shop', 'owners'])]
