# Generated by Django 3.2.5 on 2021-08-01 20:57

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('icon', models.ImageField(upload_to='photos/icons/%Y/%m/%d/')),
                ('active', models.PositiveSmallIntegerField(default=1, validators=[api.models.validate_zero_or_one])),
            ],
            options={
                'db_table': 'COURSES',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('active', models.PositiveSmallIntegerField(default=1, validators=[api.models.validate_zero_or_one])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.course')),
            ],
        ),
        migrations.CreateModel(
            name='SupplementaryMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='files/%Y/%m/%d/')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.topic')),
            ],
            options={
                'db_table': 'SUPPLEMENTARY_MATERIAL',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('question_image', models.ImageField(blank=True, upload_to='photos/question_images/%Y/%m/%d/')),
                ('active', models.PositiveSmallIntegerField(default=1, validators=[api.models.validate_zero_or_one])),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.topic')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=400)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('is_right_answer', models.BooleanField()),
                ('active', models.PositiveSmallIntegerField(default=1, validators=[api.models.validate_zero_or_one])),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.question')),
            ],
        ),
    ]
