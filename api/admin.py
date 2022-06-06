from django.contrib import admin
from .models import Curso, Material, Tema, Respuesta, Pregunta, Nivel
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse


class TopicItemInline(admin.TabularInline):
    model = Tema
    extra = 0


class QuestionItemInline(admin.TabularInline):
    model = Pregunta
    extra = 0
    exclude = ['dificultad', 'numero_pregunta']


class MaterialItemInline(admin.TabularInline):
    model = Material
    extra = 0


class AnswerItemInline(admin.TabularInline):
    model = Respuesta
    extra = 0
    exclude = ['literal']


@admin.register(Curso)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['texto','icono' ,'temas_por_materia', 'activo']
    list_editable = ['activo']
    inlines = [TopicItemInline]
    search_fields = ['texto']

    @admin.display(ordering='topics_count')
    def temas_por_materia(self, course):
        # Connect to children
        url = (
                reverse('admin:api_tema_changelist')
                + '?'
                + urlencode({
            'curso__id': str(course.id)
        }))
        if course.topics_count == 0:
            return course.topics_count
        else:
            return format_html('<a href="{}">{}</a>', url, course.topics_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            topics_count=Count('tema')
        )


@admin.register(Tema)
class TopicAdmin(admin.ModelAdmin):
    autocomplete_fields = ['curso']
    inlines = [QuestionItemInline, MaterialItemInline]
    list_display = ['texto', 'curso', 'nivel' ,'preguntas_por_tema', 'materiales_por_tema', 'activo']
    list_editable = ['activo']
    list_filter = ['curso']
    list_per_page = 10
    list_select_related = ['curso']
    # Lookup types
    search_fields = ['texto__istartswith']

    def curso(self, topic):
        # Connect to parent
        url = reverse('admin:api_curso_change', args=(topic.curso.id,))
        return format_html('<a href="{}">{}</a>', url, topic.curso.texto)

    @admin.display(ordering='questions_count')
    def preguntas_por_tema(self, topic):
        # Connect to children
        url = (
                reverse('admin:api_pregunta_changelist')
                + '?'
                + urlencode({
            'tema__id': str(topic.id)
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
            'tema__id': str(topic.id)
        }))
        if topic.material_count == 0:
            return topic.material_count
        else:
            return format_html('<a href="{}">{}</a>', url, topic.material_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            questions_count=Count('pregunta'),
            material_count=Count('material')
        )


@admin.register(Pregunta)
class QuestionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tema']
    inlines = [AnswerItemInline]
    list_display = ['texto', 'imagen', 'tema', 'respuestas', 'activo']
    list_editable = ['activo']
    list_filter = ['tema__curso', 'tema']
    list_per_page = 10
    list_select_related = ['tema']
    search_fields = ['exto__istartswith']
    exclude = ['dificultad', 'numero_pregunta']

    def tema(self, question):
        url = reverse('admin:api_tema_change', args=(question.tema.id,))
        return format_html('<a href="{}">{}</a>', url, question.tema.texto)

    @admin.display(ordering='answers_count')
    def respuestas(self, question):
        url = (
                reverse('admin:api_respuesta_changelist')
                + '?'
                + urlencode({
            'pregunta__id': str(question.id)
        }))
        if question.answers_count == 0:
            return question.answers_count
        else:
            return format_html('<a href="{}">{}</a>', url, question.answers_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            answers_count=Count('answers'),
        )


@admin.register(Respuesta)
class AnswerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['pregunta']
    list_display = ['texto', 'es_respuesta_correcta', 'pregunta', 'imagen']
    list_editable = ['es_respuesta_correcta']
    # filtering by grandparent
    # TODO: Considering if in filtering we should add 'question'
    list_filter = ['pregunta__tema']
    list_per_page = 10
    list_select_related = ['pregunta']
    search_fields = ['texto__istartswith']
    exclude = ['literal']

    def pregunta(self, answer):
        # Connect to parent
        url = reverse('admin:api_pregunta_change', args=(answer.pregunta.id,))
        return format_html('<a href="{}">{}</a>', url, answer.pregunta.texto)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tema']
    list_display = ['texto', 'archivo', 'tema', 'activo']
    list_editable = ['activo']
    list_filter = ['tema__curso', 'tema']
    list_per_page = 10
    list_select_related = ['tema']
    search_fields = ['texto__istartswith']


@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ['dificultad', 'puntos_necesarios']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False