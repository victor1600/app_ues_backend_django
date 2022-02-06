from django.contrib import admin
from .models import Course, Material, Topic, Answer, Question
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse


class TopicItemInline(admin.TabularInline):
    model = Topic
    extra = 0


class QuestionItemInline(admin.TabularInline):
    model = Question
    extra = 0


class MaterialItemInline(admin.TabularInline):
    model = Material
    extra = 0


class AnswerItemInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'temas_por_materia', 'active']
    list_editable = ['active']
    inlines = [TopicItemInline]
    search_fields = ['name']

    @admin.display(ordering='topics_count')
    def temas_por_materia(self, course):
        # Connect to children
        url = (
                reverse('admin:api_topic_changelist')
                + '?'
                + urlencode({
            'course__id': str(course.id)
        }))
        if course.topics_count == 0:
            return course.topics_count
        else:
            return format_html('<a href="{}">{}</a>', url, course.topics_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            topics_count=Count('topic')
        )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    autocomplete_fields = ['course']
    inlines = [QuestionItemInline, MaterialItemInline]
    list_display = ['name', 'curso', 'preguntas_por_tema', 'materiales_por_tema', 'active']
    list_editable = ['active']
    list_filter = ['course']
    list_per_page = 10
    list_select_related = ['course']
    # Lookup types
    search_fields = ['name__istartswith']

    def curso(self, topic):
        # Connect to parent
        url = reverse('admin:api_course_change', args=(topic.course.id,))
        return format_html('<a href="{}">{}</a>', url, topic.course.name)

    @admin.display(ordering='questions_count')
    def preguntas_por_tema(self, topic):
        # Connect to children
        url = (
                reverse('admin:api_question_changelist')
                + '?'
                + urlencode({
            'topic__id': str(topic.id)
        }))
        if topic.questions_count == 0:
            return topic.questions_count
        else:
            return format_html('<a href="{}">{}</a>', url, topic.questions_count)

    @admin.display(ordering='material_count')
    def materiales_por_tema(self, topic):
        url = (
                reverse('admin:api_material_changelist')
                + '?'
                + urlencode({
            'topic__id': str(topic.id)
        }))
        if topic.material_count == 0:
            return topic.material_count
        else:
            return format_html('<a href="{}">{}</a>', url, topic.material_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            questions_count=Count('question'),
            material_count=Count('material')
        )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['topic']
    inlines = [AnswerItemInline]
    list_display = ['question_text', 'question_image', 'tema', 'respuestas', 'active']
    list_editable = ['active']
    list_filter = ['topic__course', 'topic']
    list_per_page = 10
    list_select_related = ['topic']
    search_fields = ['question_text__istartswith']

    def tema(self, question):
        url = reverse('admin:api_topic_change', args=(question.topic.id,))
        return format_html('<a href="{}">{}</a>', url, question.topic.name)

    @admin.display(ordering='answers_count')
    def respuestas(self, question):
        url = (
                reverse('admin:api_answer_changelist')
                + '?'
                + urlencode({
            'question__id': str(question.id)
        }))
        if question.answers_count == 0:
            return question.answers_count
        else:
            return format_html('<a href="{}">{}</a>', url, question.answers_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            answers_count=Count('answers'),
        )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['question']
    list_display = ['answer_text', 'is_right_answer', 'pregunta']
    list_editable = ['is_right_answer']
    # filtering by grandparent
    # TODO: Considering if in filtering we should add 'question'
    list_filter = ['question__topic']
    list_per_page = 10
    list_select_related = ['question']
    search_fields = ['answer_text__istartswith']

    def pregunta(self, answer):
        # Connect to parent
        url = reverse('admin:api_question_change', args=(answer.question.id,))
        return format_html('<a href="{}">{}</a>', url, answer.question.question_text)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    autocomplete_fields = ['topic']
    list_display = ['name', 'file', 'topic', 'active']
    list_editable = ['active']
    list_filter = ['topic__course', 'topic']
    list_per_page = 10
    list_select_related = ['topic']
    search_fields = ['name__istartswith']
