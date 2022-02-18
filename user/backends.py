from django.contrib.auth.backends import BaseBackend
from logging import getLogger

from .models import User

logger = getLogger()


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('calling custom backend')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            if user.is_superuser:
                return user
            # TODO: do something is user is student.

        return None

    def get_user(self, id):
        return User.objects.filter(pk=id).first()
