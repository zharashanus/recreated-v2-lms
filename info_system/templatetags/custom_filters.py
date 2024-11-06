from django import template

register = template.Library()

@register.filter
def filter_schedule(schedules, weekday):
    """Фильтр для получения расписания по дню недели"""
    return schedules.filter(day_of_week=weekday).first() 