from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from api.signals import *
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum, Count
from django.db.models.functions import Coalesce

import logging

from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

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

    # TODO: CONSIDERING RETURNING EQUALLY SIZED CHUNKS OF EVERY COURSE.
    # TODO: configure limitations.
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
            notas_parciales = {}
            for a_id in answer_ids:
                answer = Respuesta.objects.get(pk=a_id)
                question = answer.pregunta

                if question.tema.curso.texto not in notas_parciales:
                    notas_parciales[question.tema.curso.texto] = []

                notas_parciales[question.tema.curso.texto].append(answer.es_respuesta_correcta)

            for k, v in notas_parciales.items():
                notas_parciales[k] = sum(v) / len(v) * 10

            grade = round(grade, 2)
            response = {"grade": grade, "partial_grades": notas_parciales,
                        }
            # TODO: implement signal history saving
            exam_finished.send_robust(sender=None, data=response, user=request.user)

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


class CandidateApiViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Aspirante.objects.annotate(score=Coalesce(Sum('examen__nota'), 0.0))\
        .annotate(n_exams_completed=Coalesce(Count('examen'),0)) \
        .order_by('-score')
    serializer_class = AspiranteSerializer

    @action(detail=False, methods=['GET', 'PATCH'])
    def me(self, request):
        if request.user.is_anonymous:
            return Response("Usuario no tiene perfil de aspirante asociado")
        logger.info(request.user)
        aspirante = get_object_or_404(self.queryset, user_id=request.user.id)
        if request.method == 'GET':
            logger.info(f'{request.user} ')
            serializer = AspiranteSerializer(aspirante, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'PATCH':
            print(aspirante)
            print(request.data)
            serializer = AspiranteSerializer(aspirante, data=request.data, partial=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

