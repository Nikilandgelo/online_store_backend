from rest_framework import serializers
from django.db.models import Model


class FinderNameField(serializers.PrimaryKeyRelatedField):
    """
    Serializer field for finding an object by its name field.

    This field allows to find an object by its name field
    and return its primary key.

    Attributes:
        model (Model): The model class to search for.
        finder_field (str): The name of the field to search for.
    """
    def __init__(self, model: Model, finder_field: str, **kwargs):
        self.model: Model = model
        self.finder_field: str = finder_field
        super().__init__(**kwargs)

    def to_internal_value(self, data) -> Model:
        """
        Convert the provided data to the related model instance.

        This method searches for an object in the related model by the
        specified field name and returns the corresponding instance.
        If the object is not found, a ValidationError
        is raised.
        """
        try:
            return self.model.objects.get(**{self.finder_field: data})
        except self.model.DoesNotExist as error:
            raise serializers.ValidationError((f'{self.model.__name__} with'
                                               f'{self.finder_field} "{data}"'
                                               f'does not exist.')) from error
