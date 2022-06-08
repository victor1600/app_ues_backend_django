from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from api.signals import *
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum, Count, F, Value
from django.db.models.functions import Coalesce, RowNumber, Rank, DenseRank
from rest_framework.pagination import PageNumberPagination
from django.db.models.expressions import RawSQL, Window

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
    filterset_fields = ['curso', 'nivel']

    # TODO: implement is_available, performing a calculation on dependents previous score.
    # TODO: Luego de lograr sacar mas de 6, tres veces en ambos temas, se desbloquea el siguiente.
    @action(detail=False, methods=['GET'])
    def get_levels(self, request):
        levels = {l.dificultad: [] for l in Nivel.objects.all()}
        topics_by_level = {**levels}
        course_id = self.request.query_params.get('curso')
        curso = Curso.objects.filter(pk=course_id).first()
        if curso:
            for topic in Tema.objects.filter(curso=curso):
                topics_by_level[topic.nivel_actual].append(TopicSerializer(topic, context={'request': request}).data)
            for level in topics_by_level.keys():
                if level == 'Intermedio':
                    basic_completed = all(map(lambda x: x['nivel_usuario_actual'] == Nivel.DIFFICULTY_ADVANCED,
                                              topics_by_level['Basico']))
                    levels[level] = basic_completed
                elif level == 'Avanzado':
                    basic_completed = all(map(lambda x: x['nivel_usuario_actual'] == Nivel.DIFFICULTY_ADVANCED,
                                              topics_by_level['Intermedio']))
                    levels[level] = basic_completed
                else:
                    # If level is basic
                    levels[level] = True
            result = []
            for k in topics_by_level.keys():
                new_level = {
                    'name': k,
                    'topics': topics_by_level[k],
                    'available': levels[k]
                }
                result.append(new_level)
            return Response(result)
        else:
            raise serializers.ValidationError("You have to send a valid course.")


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pregunta.objects.filter(activo=True)
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Respuesta.objects.all()
    serializer_class = AnswerSerializer


class ExamQuestionsAndAnswersViewSet(viewsets.ReadOnlyModelViewSet):
    # Get just active questions in the exam
    queryset = Pregunta.objects.prefetch_related('answers').filter(activo=True)
    serializer_class = ExamQuestionsAndAnswersSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tema']

    # TODO: When exam is general, configure sending  Q&A that the user has unlocked so far?
    # Consider using Bronze, silver and gold.
    def get_queryset(self):
        if 'limit' in self.request.query_params.keys():
            try:
                limit = int(self.request.query_params.get('limit'))
                if limit > 0:
                    return self.queryset.all().order_by('?')[:limit]
            except:
                # TODO: implement better logic for this validation
                logger.warning('Invalid limit query param')
        return self.queryset.all().order_by('?')


class GradeView(APIView):
    def post(self, request, format=None):
        # TODO: Si es un examen por tema, hacer calculo y almacenar puntaje en el historico.
        serializer = ExamResultSerializer(data=request.data)
        if serializer.is_valid():
            answer_ids = serializer.data.get("answers")

            grade = Respuesta.objects.filter(Q(pk__in=answer_ids) & Q(es_respuesta_correcta=True)) \
                        .count() / len(answer_ids) * 10
            notas_parciales = {}
            # TODO: SI TODAS LAS PREGUNTAS CORRESPONDEN A UN SOLO TEMA, ENTONCES CALCULAR PUNTAJE Y ACTUALIZAR
            # (TODO) EN TABLA CORRESPONDIENTE
            topics = []

            for a_id in answer_ids:
                answer = Respuesta.objects.get(pk=a_id)
                question = answer.pregunta
                topics.append(question.tema)

                if question.tema.curso.texto not in notas_parciales:
                    notas_parciales[question.tema.curso.texto] = []

                notas_parciales[question.tema.curso.texto].append(answer.es_respuesta_correcta)

            for k, v in notas_parciales.items():
                notas_parciales[k] = sum(v) / len(v) * 10

            grade = round(grade, 2)
            response = {"grade": grade, "partial_grades": notas_parciales}
            exam_finished.send_robust(sender=None, data=response, user=request.user, topics=topics)

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


class CandidateApiViewSet(viewsets.ReadOnlyModelViewSet):
    # TODO: annotate with position
    queryset = Aspirante.objects.select_related('user').annotate(score=Coalesce(Sum('examen__nota'), 0.0)) \
        .annotate(n_exams_completed=Coalesce(Count('examen'), 0)) \
        .order_by('-score').annotate(rank=Window(
        expression=DenseRank(),
        order_by=[F('score').desc(), F('id').desc()]))
    # Included id in ordering, to avoid getting duplicate ranking for same scores.
    serializer_class = AspiranteSerializer

    def list(self, request):
        # Overrode this method to only return 20, and get my current position
        students = self.get_queryset()
        serializer = AspiranteSerializer(students, many=True)
        result = serializer.data
        me = list(filter(lambda x: x['user_id'] == request.user.id, result))[0]
        return Response({'leaderboard': result[:20], 'me': me})

    @action(detail=False, methods=['GET', 'PATCH'])
    def me(self, request):
        if request.user.is_anonymous:
            return Response("Usuario no tiene perfil de aspirante asociado")
        logger.info(request.user)
        aspirante = get_object_or_404(self.queryset, user_id=request.user.id)
        aspirante.rank = None
        if request.method == 'GET':
            logger.info(f'{request.user} ')
            serializer = AspiranteSerializer(aspirante, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = AspiranteSerializer(aspirante, data=request.data, partial=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
