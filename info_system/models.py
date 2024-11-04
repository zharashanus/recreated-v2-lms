from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.html import format_html
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .group_model import Group, LessonSchedule

class Attendance(models.Model):
    student = models.ForeignKey('auth_app.StudentUser', on_delete=models.CASCADE, verbose_name='Студент', null=True)
    lesson = models.ForeignKey(LessonSchedule, on_delete=models.CASCADE, verbose_name='Урок')
    date = models.DateField(verbose_name='Дата', default=now)
    status = models.CharField(max_length=10, choices=[
        ('present', 'Присутствовал'),
        ('absent', 'Отсутствовал'),
        ('none', 'Не отмечено')
    ], default='none', verbose_name='Статус')

    class Meta:
        verbose_name = 'Посещаемость'
        verbose_name_plural = 'Посещаемость'
        unique_together = ['student', 'lesson', 'date']

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.lesson} - {self.date}"

class Grade(models.Model):
    student = models.OneToOneField('auth_app.StudentUser', on_delete=models.CASCADE, verbose_name='Студент')
    behaviour = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Поведение', default=1)
    motivation = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Мотивация', default=1)
    grade_level = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Уровень оценок', default=1)
    activities = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Активность', default=1)
    attendance = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Посещаемость', default=1)
    is_present = models.BooleanField(default=False)
    average_grade = models.FloatField(editable=False, default=0, verbose_name='Средний балл')

    def save(self, *args, **kwargs):
        total = self.behaviour + self.motivation + self.grade_level + self.activities + self.attendance
        self.average_grade = total / 5.0
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Оценки {self.student.first_name}'

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки Студентов'

class Progress(models.Model):
    POSITION_CHOICES = [
        ('INTERN', 'Intern'),
        ('JUNIOR', 'Junior'),
        ('MIDDLE', 'Middle'),
        ('SENIOR', 'Senior'),
        ('TEAMLEAD', 'TeamLead'),
    ]

    student = models.OneToOneField('auth_app.StudentUser', on_delete=models.CASCADE, verbose_name='Студент')
    progress_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name='Прогресс', default=1)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default='INTERN', verbose_name='Позиция')

    def save(self, *args, **kwargs):
        self.position = self.calculate_position()
        super().save(*args, **kwargs)

    def calculate_position(self):
        if self.progress_percentage < 25:
            return 'INTERN'
        elif 25 <= self.progress_percentage < 50:
            return 'JUNIOR'
        elif 50 <= self.progress_percentage < 75:
            return 'MIDDLE'
        elif 75 <= self.progress_percentage < 90:
            return 'SENIOR'
        else:
            return 'TEAMLEAD'

    def __str__(self):
        return f'Прогресс {self.student.first_name} - {self.get_position_display()}'

    class Meta:
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогресс Студентов'

class Achievement(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name='Награда')
    is_checked = models.BooleanField(default=False, verbose_name='Сделано')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'

class StudentAchievement(models.Model):
    student = models.ForeignKey('auth_app.StudentUser', on_delete=models.CASCADE, related_name='student_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='student_achievements')
    date_awarded = models.DateField(verbose_name='Дата получения', default=now)

    class Meta:
        unique_together = ('student', 'achievement')
        verbose_name = 'Достижение студента'
        verbose_name_plural = 'Достижения студентов'

@receiver(post_save, sender='auth_app.StudentUser')
def create_grade_for_new_student(sender, instance, created, **kwargs):
    if created:
        Grade.objects.create(student=instance)

@receiver(post_save, sender='auth_app.StudentUser')
def create_progress_for_new_student(sender, instance, created, **kwargs):
    if created:
        Progress.objects.create(student=instance)