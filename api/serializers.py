from django.db.models import Q, Avg

from rest_framework import serializers
from .models import *


class CourseSerializer(serializers.ModelSerializer):
    nota_parcial = serializers.IntegerField(read_only=True)

    class Meta:
        model = Curso
        # fields = '__all__'
        exclude = ('created_at', 'activo')


class TopicSerializer(serializers.ModelSerializer):
    nivel_usuario_actual = serializers.SerializerMethodField()


    class Meta:
        model = Tema
        fields = ('id', 'texto',  'curso', 'nivel_usuario_actual')

    def get_nivel_usuario_actual(self, obj):
        request = self.context.get('request', None)
        if request:
            aspirante = Aspirante.objects.filter(user=request.user).first()
            registro_puntuacion = PuntuacionTemaAspirante.objects.filter(tema=obj, aspirante=aspirante).first()
            if registro_puntuacion:
                return registro_puntuacion.nivel_actual
        return Nivel.DIFFICULTY_BASIC


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        exclude = ('created_at', 'activo')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        exclude = ('created_at', 'activo', 'numero_pregunta')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['texto', 'imagen']:
            try:
                if rep[field] is None or 'autogenerado' in rep[field]:
                    rep.pop(field)
            except KeyError:
                pass
        return rep


class AnswerSerializer(serializers.ModelSerializer):
    # TODO: validate there is only one question with is_right_answer set to True.
    class Meta:
        model = Respuesta
        # fields = '__all__'
        exclude = ('created_at', 'activo', 'literal',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['texto', 'imagen']:
            try:
                if rep[field] is None or 'autogenerado' in rep[field]:
                    rep.pop(field)
            except KeyError:
                pass
        return rep


class ExamQuestionsAndAnswersSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = ('id', 'texto', 'imagen', 'tema', 'answers')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['texto', 'imagen']:
            try:
                if rep[field] is None or 'autogenerado' in rep[field]:
                    rep.pop(field)
            except KeyError:
                pass
        return rep


class ExamResultSerializer(serializers.Serializer):
    answers = serializers.PrimaryKeyRelatedField(queryset=Respuesta.objects.all(), many=True)


class PartialGradeSerializer(serializers.Serializer):
    curso = serializers.CharField()
    nota = serializers.FloatField()


class AspiranteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    score = serializers.FloatField(read_only=True)
    average_grades = serializers.SerializerMethodField()
    n_exams_completed = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['rank']:
            try:
                if rep[field] is None:
                    rep.pop(field)
            except KeyError:
                pass
        return rep

    class Meta:
        model = Aspirante
        fields = ['id','imagen','first_name', 'last_name', 'score', 'average_grades',
                  'n_exams_completed', 'user_id', 'rank']

    def get_average_grades(self, obj):
        result = Curso.objects \
            .annotate(nota_parcial=Avg('examen_curso__nota')).filter(~Q(nota_parcial=None)) \
            .filter(examen_curso__examen__aspirante__id=obj.id)

        serializer = CourseSerializer(result, many=True)
        grades = [{'course': c['texto'], 'grade': round(c['nota_parcial'], 2)} for c in serializer.data]
        return grades

    # TODO: Implement consecutive days practiced


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regla
        fields = '__all__'
