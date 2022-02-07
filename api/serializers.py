from rest_framework import serializers
from .models import Curso, Material, Pregunta, Tema, Respuesta


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
        fields = ('id', 'question_text', 'question_image', 'topic',  'answers')


class ExamResultSerializer(serializers.Serializer):
    # TODO: analyze if we really need the questions.
    # question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answers = serializers.PrimaryKeyRelatedField(queryset=Respuesta.objects.all(), many=True)

