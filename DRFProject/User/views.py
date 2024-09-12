from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import LoginSerializer, RegistrationSerializer
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from .tasks import send_email
import os
from django.http import HttpResponse
from graduate_work.html_forms import RESET_PASSWORD, EMAIL_RESET_PASSWORD
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegistrationView(APIView):

    def get(self, request: Request) -> Response:
        """
        Handle GET request to confirm email address.

        :param request: The request object with token in query string.
        """
        user: User = get_object_or_404(Token,
                                       key=request.query_params.get('token')
                                       ).user
        if user.is_email_confirm:
            return Response('User is already confirmed', status=400)
        user.is_email_confirm = True
        user.save()
        return Response('User has been confirmed', status=200)

    def post(self, request: Request) -> Response:
        """
        Handle POST request to register a user.

        This function takes a request object and validates the provided data
        using the RegistrationSerializer. If the data is valid, it creates a
        new user and returns a response.
        """
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(('User has been created, now you will get a message '
                         'with confirmation, please verify your email '
                         'address.'), status=201)


@api_view(['POST'])
def login(request: Request) -> Response:
    """
    Handle POST request to login a user.

    This function takes a request object and validates the provided data using
    the LoginSerializer. If the data is valid, it checks if the user exists and
    if the provided password matches the stored one. If the password is
    correct, it takes or creates a token for the user and returns a response
    with a greeting message and the token in the headers.

    :param request: The request object with data in body.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user: User = get_object_or_404(User,
                                   email=serializer.validated_data.get('email')
                                   )
    if check_password(serializer.validated_data.get('password'),
                      user.password):
        token: tuple[Token, bool] = Token.objects.get_or_create(user=user)
        return Response(
            (f'Hello {user.first_name}! You are proofed that '
             'you are registered. Your token is in headers.'),
            status=200,
            headers={'Authorization': f'Token {token[0].key}'})
    else:
        return Response('Password is not correct', status=400)


class ResetPasswordView(APIView):
    """
    View class to handle reset password requests.

    This class has two methods: get and post.
    The get method returns a web page with a form for entering a new password.
    The post method takes a request object and validates the provided data.
    If the data is valid, it sends an email with a link to the user.
    """
    def get(self, request: Request) -> Response:
        """
        Handle GET request to reset password.

        :param request: The request object with token in query string.
        :return: A web page with a form for entering a new password.
        """
        url: str = (f'{os.getenv("SERVER_SOCKET")}{reverse("change_password")}'
                    f'?token={request.query_params.get("token")}')
        return HttpResponse(RESET_PASSWORD.format(url=url),
                            content_type='text/html')

    def post(self, request: Request) -> Response:
        """
        Handle POST request to send email with link to form for reset password.

        :param request: The request object with data in body.
        """
        user: User = get_object_or_404(User, email=request.data.get('email'))
        url: str = (f'{os.getenv("SERVER_SOCKET")}'
                    f'{reverse("ask_reset_password")}'
                    f'?token={user.auth_token.key}')
        send_email.delay(
            title='Password Reset', email=user.email,
            html_message=EMAIL_RESET_PASSWORD.format(url=url))
        return Response('Check your email', status=200)


@api_view(['POST'])
def change_password(request: Request) -> Response:
    """
    Handle POST request to change password.

    :param request: The request object with data in body and
    token in query string.
    """
    user: User = get_object_or_404(Token,
                                   key=request.query_params.get('token')).user
    new_password = request.data.get('password')
    if not new_password:
        return Response('Please enter new password', status=400)
    try:
        validate_password(new_password)
    except ValidationError as error:
        return Response(error.messages[0], status=400)
    user.password = make_password(new_password)
    user.save()
    return Response('Password has been changed', status=200)
