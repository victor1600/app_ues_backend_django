# Generated by Django 3.2.15 on 2022-08-26 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aspirante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_de_nacimiento', models.DateField(blank=True, null=True)),
                ('imagen', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('icono', models.ImageField(upload_to='photos/icons/%Y/%m/%d/')),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['texto', 'created_at'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricoExamen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.FloatField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('aspirante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examen', to='api.aspirante')),
            ],
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dificultad', models.CharField(choices=[('Basico', 'Basico'), ('Intermedio', 'Intermedio'), ('Avanzado', 'Avanzado')], default='Basico', max_length=15, unique=True)),
                ('puntos_necesarios', models.FloatField(max_length=6)),
            ],
            options={
                'verbose_name_plural': 'niveles',
            },
        ),
        migrations.CreateModel(
            name='Regla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('info', models.TextField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='photos/rules/%Y/%m/%d/')),
                ('type', models.CharField(choices=[('Tema', 'Tema'), ('Curso', 'Curso')], default='Curso', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('activo', models.BooleanField(default=True)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.curso')),
                ('nivel', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='api.nivel')),
            ],
            options={
                'ordering': ['texto', 'created_at'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='photos/question_images/%Y/%m/%d/')),
                ('activo', models.BooleanField(default=True)),
                ('numero_pregunta', models.IntegerField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('Opción múltiple', 'Opción múltiple'), ('Complementar', 'Complementar')], default='Opción múltiple', max_length=255)),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tema')),
            ],
            options={
                'managed': True,
                'unique_together': {('texto', 'tema', 'numero_pregunta')},
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('archivo', models.FileField(max_length=2000, upload_to='files/%Y/%m/%d/')),
                ('activo', models.BooleanField(default=True)),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tema')),
            ],
            options={
                'verbose_name_plural': 'materiales',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricoExamenCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.FloatField(max_length=4)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examen_curso', to='api.curso')),
                ('examen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examen', to='api.historicoexamen')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=600, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('es_respuesta_correcta', models.BooleanField()),
                ('activo', models.BooleanField(default=True)),
                ('literal', models.CharField(blank=True, max_length=2, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='photos/answer_images/%Y/%m/%d/')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='api.pregunta')),
            ],
            options={
                'managed': True,
                'unique_together': {('pregunta', 'literal')},
            },
        ),
        migrations.CreateModel(
            name='PuntuacionTemaAspirante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.FloatField(default=0.0, max_length=4)),
                ('aspirante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.aspirante')),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tema')),
            ],
            options={
                'unique_together': {('tema', 'aspirante')},
            },
        ),
    ]
