from django.shortcuts import render
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


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
