from django.contrib.auth.backends import BaseBackend
from logging import getLogger

from api.models import Aspirante
from .models import User
from app_ues_backend_django.utils.ues_auth import authenticate_ues_student

logger = getLogger()


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.info('calling custom backend')
        user = User.objects.filter(username=username).first()

        if not user:
            student_data = authenticate_ues_student(username, password)
            if student_data:
                password = student_data.pop('password')
                new_user = User.objects.create(**student_data)
                new_user.set_password(password)
                new_user.save()
                Aspirante.objects.create(user=new_user)
                logger.info(f'New user was created: {new_user}')
                return new_user

        if user and user.check_password(password):
            # if user.is_superuser:
            return user
            # TODO: do something is user is student.

        return None

    def get_user(self, id):
        return User.objects.filter(pk=id).first()
