# Generated by Django 5.1.2 on 2024-11-03 20:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя:')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия:')),
                ('specialization', models.CharField(max_length=200, verbose_name='Специализация:')),
                ('experience_years', models.IntegerField(verbose_name='Опыт работы (лет):')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='mentor_avatars/', verbose_name='Аватарка')),
                ('bio', models.TextField(blank=True, verbose_name='Биография:')),
            ],
            options={
                'verbose_name': 'Ментор',
                'verbose_name_plural': 'Менторы',
            },
        ),
        migrations.CreateModel(
            name='StudentUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100, verbose_name='Имя:')),
                ('last_name', models.CharField(default='', max_length=100, verbose_name='Фамилия:')),
                ('age', models.IntegerField(default=1, verbose_name='Возраст')),
                ('contact_name', models.CharField(max_length=100, verbose_name='Контактное имя:')),
                ('contact_number', models.CharField(max_length=15, verbose_name='Контактный номер:')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Аватарка')),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя:')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия:')),
                ('specialization', models.CharField(max_length=200, verbose_name='Специализация:')),
                ('experience', models.IntegerField(verbose_name='Опыт работы (лет):')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='manager_avatars/', verbose_name='Аватарка')),
                ('bio', models.TextField(blank=True, verbose_name='Биография:')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='manager_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Менеджер',
                'verbose_name_plural': 'Менеджеры',
            },
        ),
    ]
