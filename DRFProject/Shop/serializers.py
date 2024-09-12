from rest_framework import serializers
from rest_framework.serializers import StringRelatedField
from graduate_work.relations import FinderNameField
from .models import Shop, ShopCategories, ShopOwners
from Categories.models import Category
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.db.utils import IntegrityError
from django.db import transaction
from rest_framework.serializers import ValidationError
from Order.serializers import GetOrderSerializer


class ShopSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Shop model.

    This class is used to serialize the name, categories, and owners of a shop.
    It also provides the logic for creating and updating shops.
    """
    categories = FinderNameField(
        model=Category, finder_field='name', many=True,
        queryset=Category.objects.all())
    owners = FinderNameField(
        model=get_user_model(), finder_field='email', many=True,
        queryset=get_user_model().objects.all())
    products = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Shop
        fields: list[str] = ['name', 'categories', 'owners', 'products',
                             'is_accepting_orders']

    def validate_categories(self, value: list) -> list:
        if not value:
            raise serializers.ValidationError('Categories cannot be empty')
        return value

    def create(self, validated_data: dict) -> Shop:
        try:
            with transaction.atomic():
                accepting_orders = validated_data.pop(
                    'is_accepting_orders', True)

                created_shop: Shop = Shop.objects.create(
                    name=validated_data.pop('name'),
                    is_accepting_orders=accepting_orders)

                self.creating_related_objects(
                    validated_data.pop('categories'), ShopCategories,
                    created_shop, 'category')

                owners: list = validated_data.pop('owners')
                owners.append(self.context.pop('request').user)
                self.creating_related_objects(
                    owners, ShopOwners, created_shop, 'owner')

                return created_shop
        except IntegrityError as error:
            raise ValidationError(str(error)) from error

    def update(self, instance: Shop, validated_data: dict) -> Shop:
        try:
            with transaction.atomic():
                instance.name = validated_data.pop('name')

                accepting_orders = validated_data.pop(
                    'is_accepting_orders', True)
                instance.is_accepting_orders = accepting_orders
                instance.save()

                ShopCategories.objects.filter(shop=instance).delete()
                ShopOwners.objects.filter(shop=instance).exclude(
                    owner=self.context.get('request').user).delete()

                self.creating_related_objects(
                    validated_data.pop('categories'), ShopCategories,
                    instance, 'category')
                self.creating_related_objects(
                    validated_data.pop('owners'), ShopOwners,
                    instance, 'owner')
                return instance
        except IntegrityError as error:
            raise ValidationError(str(error)) from error

    @staticmethod
    def creating_related_objects(related_objects: list,
                                 model_related_objects: Model,
                                 shop_instance: Shop, related_field_name: str):
        """
        Creates related objects (categories or owners) for a shop instance.
        """
        for related_instance in related_objects:
            model_related_objects.objects.create(
                shop=shop_instance, **{related_field_name: related_instance})


class ShopProductsOrders(serializers.Serializer):
    order = GetOrderSerializer()
