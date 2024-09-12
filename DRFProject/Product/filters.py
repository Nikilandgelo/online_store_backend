from django_filters import rest_framework
from Shop.models import Shop
from Categories.models import Category
from django.utils.functional import lazy


def get_shops() -> list[tuple[str, str]]:
    return [(shop.name, shop.name) for shop in Shop.objects.all()]


def get_categories() -> list[tuple[str, str]]:
    return [(category.name, category.name)
            for category in Category.objects.all()]


class ProductFilterSet(rest_framework.FilterSet):
    shop_name = rest_framework.ChoiceFilter(
        field_name='shop__name',
        choices=lazy(get_shops, list))
    category = rest_framework.ChoiceFilter(
        field_name='shop__categories__name',
        choices=lazy(get_categories, list))
    name = rest_framework.CharFilter(
        field_name='name', lookup_expr='istartswith')
    price_min = rest_framework.NumberFilter(
        field_name='price', lookup_expr='gte')
    price_max = rest_framework.NumberFilter(
        field_name='price', lookup_expr='lte')
