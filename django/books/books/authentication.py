from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import authentication, exceptions


class InsecureTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or 'Bearer' not in auth_header:
            return None
        username = auth_header.split()[1]
        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist as exc:
            raise exceptions.AuthenticationFailed('No such user') from exc

        return (user, None)
