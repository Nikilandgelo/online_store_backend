from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.db.models import Model


def IsOwnerOrReadOnlyOrAdmin(path_to_owners: list):
    """
    Permission class for checking if the object's owner is the same as the user
    or if the user is a superuser or if the request method is a safe method.

    Args:
        path_to_owners (list): A list of fields to traverse to find the owners
        of the object.
    """
    class WrapperContent(BasePermission):
        def has_object_permission(self, request, view, obj: Model) -> bool:
            if request.method in SAFE_METHODS or request.user.is_superuser:
                return True

            owners: Model = obj
            for field in path_to_owners:
                owners = getattr(owners, field)
            return request.user in owners.all()

    return WrapperContent
