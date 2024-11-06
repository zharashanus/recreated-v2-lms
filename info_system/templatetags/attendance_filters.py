from django import template

register = template.Library()

@register.filter
def get_schedule(schedules, weekday):
    """Получить расписание для конкретного дня недели"""
    return schedules.filter(day_of_week=weekday).first()

@register.filter
def get_attendance_status(attendance_data, date):
    """Получить статус посещаемости для конкретной даты"""
    return attendance_data.get(date, {}).get('status', 'UNKNOWN') 