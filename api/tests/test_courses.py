import logging
from rest_framework import status
from api.signals import test_finished
from api.models import Curso
from model_bakery import baker
from django.conf import settings
import requests
from PIL import Image
from io import StringIO

import pytest

logger = logging.getLogger()


# @pytest.fixture
# def create_course(api_client):
#     def do_create_course(course):
#         # TODO: create objects using Objects.
#         image_url = f'{settings.BASE_DIR}/icons/biologia.png'
#         response = api_client.post('/api/courses/', {**course,
#                                           'icono': open(image_url, 'rb')})
#         # We can supply additional data using **kwargs
#         if 'icono' in response.data:
#             media_url_partial_path = response.data['icono'].split("testserver/")[1]
#             # TODO: fix this:
#             test_finished.send_robust(sender=None, media_url=media_url_partial_path)
#         logger.info(response.status_code)
#         return response
#     return do_create_course


# @pytest.mark.django_db
# class TestCreateCourse:
#     def test_if_user_is_anonymous_returns_401(self, api_client, create_course, authenticate):
#         # authenticate()
#         # TODO: Put this into a func
#         response = create_course({'texto': 'a'})
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestRetrieveCourse:
    @pytest.mark.skip
    def test_if_user_is_anonymous_returns_401(self, api_client):
        course = baker.make(Curso)
        response = api_client.get(f'/api/courses/{course.id}/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_course_exists_returns_200(self, api_client, authenticate):
        course = baker.make(Curso)
        authenticate()
        response = api_client.get(f'/api/courses/{course.id}/')
        print(response.data['icono'])
        assert False
        assert response.status_code == status.HTTP_200_OK

        # TODO: create test case to test if img is visible!!
    # def test_img_visible(self, api_client, authenticate):
    #     image_url = f'{settings.BASE_DIR}/icons/biologia.png'
    #     course = Curso.objects.create(texto='a', icono=image_url)
    #     authenticate()
    #     response = api_client.get(f'/api/courses/{course.id}/')
    #     print(response.data['icono'])
    #     r = requests.get(response.data['icono'])
    #     print(r.content)
    #     assert False

