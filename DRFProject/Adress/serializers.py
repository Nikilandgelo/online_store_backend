from rest_framework.serializers import ModelSerializer
from .models import Address


class AdressSerializer(ModelSerializer):
    """
    A serializer class for the Address model.

    This class is used to serialize the city, street, house number,
    hull building, and apartment of an address.

    Attributes:
        model (Address): The model to be serialized.
        fields (list[str]): A list of the model fields to be serialized.
    """

    class Meta:
        model = Address
        fields = ['city', 'street', 'house_number', 'hull_building',
                  'apartment']
