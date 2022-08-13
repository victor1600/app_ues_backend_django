from django.db import models
from django.conf import settings


# Create your models here.
class Curso(models.Model):
    texto = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    # All images/files get upload to media folder, but here,
    # we define the actual folder well be using inside the media folder.
    icono = models.ImageField(upload_to='photos/icons/%Y/%m/%d/')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.texto

    class Meta:
        managed = settings.MANAGED
        # TODO: refactor table names
        ordering = ['texto', 'created_at']


class Nivel(models.Model):
    DIFFICULTY_BASIC = 'Basico'
    DIFFICULTY_INTERMEDIATE = 'Intermedio'
    DIFFICULTY_ADVANCED = 'Avanzado'

    DIFFICULTY_LEVELS = [
        (DIFFICULTY_BASIC, 'Basico'),
        (DIFFICULTY_INTERMEDIATE, 'Intermedio'),
        (DIFFICULTY_ADVANCED, 'Avanzado'),
    ]
    dificultad = models.CharField(max_length=15, choices=DIFFICULTY_LEVELS, default=DIFFICULTY_BASIC, unique=True)
    puntos_necesarios = models.FloatField(max_length=6)

    class Meta:
        verbose_name_plural = "niveles"

    def __str__(self):
        return self.dificultad


class Tema(models.Model):
    # TODO: analyze if should be unique or not...
    texto = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.texto

    @property
    def nivel_actual(self):
        return self.nivel.dificultad if self.nivel else Nivel.objects.filter(pk=1).first().dificultad

    class Meta:
        managed = settings.MANAGED
        ordering = ['texto', 'created_at']


class Material(models.Model):
    texto = models.TextField(unique=True)
    descripcion = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    archivo = models.FileField(upload_to='files/%Y/%m/%d/', max_length=2000)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.texto

    class Meta:
        managed = settings.MANAGED
        verbose_name_plural = "materiales"


class Pregunta(models.Model):
    texto = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    imagen = models.ImageField(upload_to='photos/question_images/%Y/%m/%d/', null=True, blank=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    numero_pregunta = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.texto:
            return self.texto
        else:
            return 'Sin texto'

    class Meta:
        managed = settings.MANAGED
        unique_together = ('texto', 'tema', 'numero_pregunta')


class Respuesta(models.Model):
    texto = models.CharField(max_length=600, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='answers')
    es_respuesta_correcta = models.BooleanField()
    activo = models.BooleanField(default=True)
    # TODO: consider adding 'literal field'
    literal = models.CharField(max_length=2, null=True, blank=True)
    imagen = models.ImageField(upload_to='photos/answer_images/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        if self.texto:
            return self.texto
        else:
            return 'Sin texto'

    class Meta:
        managed = settings.MANAGED
        unique_together = ('pregunta', 'literal')


class Aspirante(models.Model):
    fecha_de_nacimiento = models.DateField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagen = models.TextField(null=True, blank=True)

    # TODO: implement profile picture
    # DISPLAY DEFAULT IMAGE IN FRONTEND IF NO IMAGE SET BY USER FOUND.

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class PuntuacionTemaAspirante(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    aspirante = models.ForeignKey(Aspirante, on_delete=models.CASCADE)
    puntuacion = models.FloatField(max_length=4, default=0.0)

    class Meta:
        unique_together = ('tema', 'aspirante',)

    def __str__(self):
        return f'id={self.id} tema={self.tema}, aspirante={self.aspirante}, puntuacion={self.puntuacion}'

    @property
    def nivel_actual(self):
        return Nivel.objects.order_by('-puntos_necesarios')\
            .filter(puntos_necesarios__lte=self.puntuacion).first().dificultad


class HistoricoExamen(models.Model):
    nota = models.FloatField(max_length=4)
    aspirante = models.ForeignKey(Aspirante, on_delete=models.CASCADE, related_name='examen')
    created_at = models.DateTimeField(auto_now=True, blank=True)


class HistoricoExamenCurso(models.Model):
    examen = models.ForeignKey(HistoricoExamen, on_delete=models.CASCADE, related_name='examen')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='examen_curso')
    nota = models.FloatField(max_length=4)


class Regla(models.Model):
    TYPE_TOPIC = 'Tema'
    TYPE_COURSE = 'Curso'

    DIFFICULTY_LEVELS = [
        (TYPE_TOPIC, 'Tema'),
        (TYPE_COURSE, 'Curso'),
    ]
    name = models.CharField(max_length=255)
    info = models.TextField()
    imagen = models.ImageField(upload_to='photos/rules/%Y/%m/%d/', null=True, blank=True)
    type = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='Curso')

    def __str__(self):
        return self.info
