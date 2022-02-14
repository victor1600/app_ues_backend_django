from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

import logging

from rest_framework.viewsets import GenericViewSet

from .serializers import *
from .models import *
from rest_framework import viewsets, status

logger = logging.getLogger(__name__)


# Create your views here.
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    # When getting elements, just the actives ones will be returned
    queryset = Curso.objects.filter()
    serializer_class = CourseSerializer


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.filter(activo=True)
    serializer_class = MaterialSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tema']


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tema.objects.filter(activo=True)
    serializer_class = TopicSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['curso']


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pregunta.objects.filter(activo=True)
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Respuesta.objects.all()
    serializer_class = AnswerSerializer


class ExamQuestionsAndAnswersViewSet(viewsets.ReadOnlyModelViewSet):
    # Get just active questions in the exam
    queryset = Pregunta.objects.filter(activo=True)
    serializer_class = ExamQuestionsAndAnswersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tema']

    def get_queryset(self):
        if 'limit' in self.request.query_params.keys():
            try:
                limit = int(self.request.query_params.get('limit'))
                if limit > 0:
                    return self.queryset.all().order_by('?')[:limit]
            except:
                # TODO: implement better logic for this validation
                logger.warning('Invalid limit query param')
                pass
        return self.queryset.all().order_by('?')


class GradeView(APIView):
    def post(self, request, format=None):
        serializer = ExamResultSerializer(data=request.data)
        if serializer.is_valid():
            answer_ids = serializer.data.get("answers")

            grade = Respuesta.objects.filter(Q(pk__in=answer_ids) & Q(es_respuesta_correcta=True)) \
                        .count() / len(answer_ids) * 10
            return Response({"grade": round(grade, 2)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AspiranteViewSet(CreateModelMixin, RetrieveModelMixin,UpdateModelMixin, GenericViewSet):
    queryset = Aspirante.objects.all()
    serializer_class = AspiranteSerializer