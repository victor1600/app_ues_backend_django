from rest_framework import serializers
from .models import *


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    # TODO: validate there is only one question with is_right_answer set to True.
    class Meta:
        model = Respuesta
        fields = '__all__'


class ExamQuestionsAndAnswersSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = ('id', 'texto', 'imagen', 'tema',  'answers')


class ExamResultSerializer(serializers.Serializer):
    # TODO: analyze if we really need the questions.
    # question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answers = serializers.PrimaryKeyRelatedField(queryset=Respuesta.objects.all(), many=True)


class AspiranteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Aspirante
        fields = ['id', 'user_id', 'fecha_de_nacimiento']
