from rest_framework.serializers import ModelSerializer
from .models import Parameter


class ParameterSerializer(ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['name', 'value']
