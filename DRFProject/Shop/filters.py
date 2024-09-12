from django_filters import rest_framework
from Categories.models import Category
from django.utils.functional import lazy


def get_categories() -> list[tuple[str, str]]:
    return [(category.name, category.name)
            for category in Category.objects.all()]


class ShopFilterSet(rest_framework.FilterSet):
    name = rest_framework.CharFilter(
        field_name='name', lookup_expr='istartswith')
    category = rest_framework.ChoiceFilter(
        field_name='categories__name',
        choices=lazy(get_categories, list))
