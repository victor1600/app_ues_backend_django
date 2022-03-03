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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['texto', 'imagen']:
            try:
                print('autogenerado' in rep[field])
                if rep[field] is None or 'autogenerado' in rep[field]:
                    rep.pop(field)
            except KeyError:
                pass
        return rep


class AnswerSerializer(serializers.ModelSerializer):
    # TODO: validate there is only one question with is_right_answer set to True.
    class Meta:
        model = Respuesta
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['texto', 'imagen']:
            try:
                if rep[field] is None or 'autogenerado' in rep[field]:  # checks if value is 'None', this is different from "emptiness"
                    rep.pop(field)
            except KeyError:
                pass
        return rep


class ExamQuestionsAndAnswersSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = ('id', 'texto', 'imagen', 'tema',  'answers')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in ['texto', 'imagen']:
            try:
                if rep[field] is None or 'autogenerado' in rep[field]:  # checks if value is 'None', this is different from "emptiness"
                    rep.pop(field)
            except KeyError:
                pass
        return rep


class ExamResultSerializer(serializers.Serializer):
    # TODO: analyze if we really need the questions.
    # question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    answers = serializers.PrimaryKeyRelatedField(queryset=Respuesta.objects.all(), many=True)


class AspiranteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Aspirante
        fields = ['id', 'user_id', 'fecha_de_nacimiento']
