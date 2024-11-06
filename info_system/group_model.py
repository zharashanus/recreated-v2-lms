from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название группы')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    mentor = models.ManyToManyField(
        'auth_app.Mentor',
        related_name='groups',
        blank=True,
        verbose_name='Менторы'
    )
    # TODO: Раскомментировать после добавления приложения code_tester
    # coding_tasks = models.ManyToManyField('code_tester.CodingTask', blank=True, related_name='assigned_groups', verbose_name='Задачи по программированию')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

class LessonSchedule(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lesson_schedules')
    day_of_week = models.IntegerField(choices=[
        (0, 'Понедельник'),
        (1, 'Вторник'),
        (2, 'Среда'),
        (3, 'Четверг'),
        (4, 'Пятница'),
        (5, 'Суббота'),
        (6, 'Воскресенье'),
    ], verbose_name='День недели')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    class Meta:
        verbose_name = 'Расписание урока'
        verbose_name_plural = 'Расписание уроков'
        unique_together = ['group', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.group.name} - {self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"