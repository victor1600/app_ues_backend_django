from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import CourseSerializer, SupplementaryMaterialSerializer, TopicSerializer, QuestionSerializer, \
    AnswerSerializer
from .models import Course, SupplementaryMaterial, Topic, Question, Answer
from rest_framework import viewsets


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SupplementaryMaterialViewSet(viewsets.ModelViewSet):
    queryset = SupplementaryMaterial.objects.all()
    serializer_class = SupplementaryMaterialSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic']


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course']


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
