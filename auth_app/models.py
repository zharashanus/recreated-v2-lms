from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.html import format_html
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentUser(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PAID', 'Оплачено'),
        ('UNPAID', 'Неоплачено'),
        ('TRIAL', 'Пробный урок'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя:', default="")
    last_name = models.CharField(max_length=100, verbose_name='Фамилия:', default="")
    age = models.IntegerField(verbose_name='Возраст', default=1)
    contact_name = models.CharField(max_length=100, verbose_name='Контактное имя:')
    contact_number = models.CharField(max_length=15, verbose_name='Контактный номер:')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватарка')
    group = models.ForeignKey('info_system.Group', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Группа')
    achievements = models.ManyToManyField('info_system.Achievement', related_name='students', blank=True, verbose_name='Достижения')
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='UNPAID',
        verbose_name='Статус оплаты'
    )

    def avatar_tag(self):
        if self.avatar:
            return format_html('<img src="{}" style="width:90px; height:auto;"/>', self.avatar.url)
        return "No image"
    avatar_tag.short_description = 'Avatar'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

class Mentor(models.Model):
    REPORT_STATUS_CHOICES = [
        ('REPORTED', 'Отчет сдан'),
        ('UNREPORTED', 'Отчет не сдан'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    first_name = models.CharField(max_length=100, verbose_name='Имя:')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия:')
    specialization = models.CharField(max_length=200, verbose_name='Специализация:')
    experience_years = models.IntegerField(verbose_name='Опыт работы (лет):')
    avatar = models.ImageField(upload_to='mentor_avatars/', blank=True, null=True, verbose_name='Аватарка')
    bio = models.TextField(verbose_name='Биография:', blank=True)
    report_status = models.CharField(
        max_length=10,
        choices=REPORT_STATUS_CHOICES,
        default='UNREPORTED',
        verbose_name='Статус отчета'
    )
    groups = models.ManyToManyField('info_system.Group', 
        blank=True, 
        related_name='assigned_mentors',
        verbose_name='Назначенные группы'
    )

    def avatar_tag(self):
        if self.avatar:
            return format_html('<img src="{}" style="width:90px; height:auto;"/>', self.avatar.url)
        return "No image"
    avatar_tag.short_description = 'Avatar'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Менторы'

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    first_name = models.CharField(max_length=100, verbose_name='Имя:')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия:')
    specialization = models.CharField(max_length=200, verbose_name='Специализация:')
    experience = models.IntegerField(verbose_name='Опыт работы (лет):')
    avatar = models.ImageField(upload_to='manager_avatars/', blank=True, null=True, verbose_name='Аватарка')
    bio = models.TextField(verbose_name='Биография:', blank=True)

    def avatar_tag(self):
        if self.avatar:
            return format_html('<img src="{}" style="width:90px; height:auto;"/>', self.avatar.url)
        return "No image"
    avatar_tag.short_description = 'Avatar'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

