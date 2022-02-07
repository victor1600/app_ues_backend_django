from django.db import models
from django.conf import settings


# Create your models here.
class Curso(models.Model):
    texto = models.CharField(max_length=50, unique=True)
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
        ordering = ['texto','created_at']


class Tema(models.Model):
    # TODO: analyze if should be unique or not...
    texto = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.texto

    class Meta:
        managed = settings.MANAGED
        ordering = ['texto', 'created_at']


class Material(models.Model):
    texto = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    archivo = models.FileField(upload_to='files/%Y/%m/%d/')
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.texto

    class Meta:
        managed = settings.MANAGED


class Pregunta(models.Model):
    texto = models.TextField()
    created_at = models.DateTimeField(auto_now=True, blank=True)
    # TODO: fix this.
    imagen = models.ImageField(upload_to='photos/question_images/%Y/%m/%d/', blank=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.texto

    class Meta:
        managed = settings.MANAGED


class Respuesta(models.Model):
    texto = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='answers')
    es_respuesta_correcta = models.BooleanField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.texto

    class Meta:
        managed = settings.MANAGED
