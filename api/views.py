from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
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

    @action(detail=True, methods=['GET'])
    def current_user_level(self, request, pk):
        topic = TopicSerializer(Tema.objects.filter(pk=pk).first(), context={'request': request}).data
        return Response({"current_level": topic['nivel_usuario_actual']})

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
                    if topics_by_level['Basico']:
                        completed = all(map(lambda x: x['nivel_usuario_actual'] == Nivel.DIFFICULTY_ADVANCED,
                                            topics_by_level['Basico']))
                        levels[level] = completed
                    else:
                        levels[level] = False
                elif level == 'Avanzado':
                    if topics_by_level['Intermedio']:
                        completed = all(map(lambda x: x['nivel_usuario_actual'] == Nivel.DIFFICULTY_ADVANCED,
                                            topics_by_level['Intermedio']))

                        levels[level] = completed
                    else:
                        levels[level] = False
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
                if k == 'Intermedio' and levels['Avanzado']:
                    new_level['available'] = True

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
        if "questions" not in request.data.keys():
            raise ValidationError("Please send questions ids in the body.")
        questions = request.data["questions"]
        question_ids_serializers = QuestionIdsSerializer(data={"questions": questions})
        question_ids_serializers.is_valid(raise_exception=True)
        question_ids = question_ids_serializers.data.get("questions")
        if "answers" not in request.data.keys():
            raise ValidationError("Please send answers ids in the body.")

        if len(request.data["questions"]) != len(request.data["answers"]):
            raise ValidationError("Please send same length of answers and questions.")
        only_multiple_choice_answers = [a for a in request.data["answers"] if isinstance(a, int)]
        string_answers = [a for a in request.data["answers"] if isinstance(a, str)]
        string_ids = []
        for string_answer in string_answers:
            string_id = [i[0] for i in Respuesta.objects.filter(texto__iexact=string_answer).values_list('id')]
            if not string_id:
                string_ids.append(None)
            else:
                string_ids.extend(string_id)

        print(string_ids)

        serializer = MultipleChoiceAnswersSerializer(data={"answers": only_multiple_choice_answers})
        if serializer.is_valid():
            answer_ids = serializer.data.get("answers") + string_ids
            question_answer_ids = [[q, a] for q, a in zip(question_ids, answer_ids)]

            if len(answer_ids) == 0:
                # Raising a validation error.
                raise ValidationError("Please send at least one answer. Either an id, or a text.")

            grade = Respuesta.objects.filter(Q(pk__in=answer_ids) & Q(es_respuesta_correcta=True)) \
                        .count() / len(request.data["answers"]) * 10
            notas_parciales = {}
            topics = []
            for q_id, a_id in zip(question_ids, answer_ids):
                answer = Respuesta.objects.filter(pk=a_id).first()
                question = Pregunta.objects.get(pk=q_id)
                topics.append(question.tema)

                if question.tema.curso.texto not in notas_parciales:
                    notas_parciales[question.tema.curso.texto] = []

                if answer:
                    notas_parciales[question.tema.curso.texto].append(answer.es_respuesta_correcta)
                else:
                    notas_parciales[question.tema.curso.texto].append(False)

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


class RulesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Regla.objects.all()
    serializer_class = RuleSerializer
