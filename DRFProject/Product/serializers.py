from rest_framework.serializers import ModelSerializer
from .models import Product
from Parameter.serializers import ParameterSerializer
from Parameter.models import Parameter
from rest_framework.serializers import StringRelatedField
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.serializers import ValidationError


class ProductSerializer(ModelSerializer):
    parameters = ParameterSerializer(many=True)
    shop = StringRelatedField()

    class Meta:
        model = Product
        fields: str = ['name', 'shop', 'quantity', 'price', 'description',
                       'parameters']

    def create(self, validated_data: dict):
        try:
            with transaction.atomic():
                parameters: list = validated_data.pop('parameters')
                product: Product = Product.objects.create(**validated_data)
                return self.creating_parameters(parameters, product)
        except IntegrityError as error:
            raise ValidationError(str(error)) from error

    def update(self, instance: Product, validated_data: dict):
        try:
            with transaction.atomic():
                parameters: list = validated_data.pop('parameters')
                for name, value in validated_data.items():
                    setattr(instance, name, value)
                instance.save()

                Parameter.objects.filter(product=instance).delete()
                return self.creating_parameters(parameters, instance)
        except IntegrityError as error:
            raise ValidationError(str(error)) from error

    @staticmethod
    def creating_parameters(parameters: list[dict | None], product: Product):
        for parameter in parameters:
            Parameter.objects.create(product=product, **parameter)
        return product
