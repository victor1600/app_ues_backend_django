from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .models import  *
from rest_framework import viewsets, status


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


class ExamQuestionsAndAnswersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = ExamQuestionsAndAnswersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic']

    def get_queryset(self):
        if 'limit' in self.request.query_params.keys():
            try:
                limit = int(self.request.query_params.get('limit'))
                if limit > 0:
                    return self.queryset.all().order_by('?')[:limit]
            except:
                # TODO: implement better logic for this validation
                print('Invalid limit query param')
                pass
        return self.queryset.all().order_by('?')


class GradeView(APIView):
    def post(self, request, format=None):
        serializer = ExamResultSerializer(data=request.data)
        if serializer.is_valid():
            answer_ids = serializer.data.get("answers")
            print(answer_ids)
            print(len(answer_ids))
            # answer_ids = [answer_id.get('answer') for answer_id in serializer.data]
            grade = Answer.objects.filter(Q(pk__in=answer_ids) & Q(is_right_answer=True))\
                        .count()/len(answer_ids) * 10
            return Response({"grade": grade}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
