from rest_framework import serializers
from rest_framework.serializers import StringRelatedField
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Category model.
    """
    shops = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields: str = ['name', 'shops']
