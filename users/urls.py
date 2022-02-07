from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls import url

router = DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    url(r'login', views.UserLoginView.as_view()),
]