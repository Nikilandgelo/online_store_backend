from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, HttpRequest
from rest_framework.authtoken.models import Token
from User.models import User
from rest_framework.permissions import SAFE_METHODS


class EmailConfirmationMiddleware(MiddlewareMixin):
    """
    Middleware to check if the user email is confirmed.

    If the user email is not confirmed, the middleware
    will return a HttpResponse with a 400 status code.
    """
    def process_request(self, request: HttpRequest) -> HttpResponse | None:
        auth_header: str | None = request.headers.get('Authorization')
        if not auth_header or request.method in SAFE_METHODS:
            return None

        try:
            token_type, token_key = auth_header.split()
            if token_type.lower() != 'token':
                return HttpResponse('Invalid token type', status=400)

            user: User = Token.objects.get(key=token_key).user
            if not user.is_email_confirm and not user.is_superuser:
                return HttpResponse('Your email is not confirmed', status=400)

        except (ValueError, Token.DoesNotExist):
            return HttpResponse('Invalid token', status=400)

        return None
