from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AdressSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError


class AdressView(APIView):
    """
    API view to create an adress for a user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        If the user already have 5 or more adresses, return 400 status code
        with an error message.

        If the data provided is invalid, return 400 status code with a message
        explaining the error.

        If the data is valid, create the adress and return 200 status code with
        a message saying that the adress has been created.
        """
        if request.user.addresses.count() >= 5:
            return Response('You can not have more than 5 adresses', 400)

        serializer = AdressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = request.user
        try:
            serializer.create(serializer.validated_data)
        except IntegrityError as error:
            return Response(str(error), 400)
        return Response('Adress has been created', 200)
