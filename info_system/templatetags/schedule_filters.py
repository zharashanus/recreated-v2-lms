from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 'none')

@register.filter
def get_attendance_status_class(status):
    status_classes = {
        'present': 'text-success',  # Присутствовал - зеленый
        'absent': 'text-danger',    # Отсутствовал - красный
        'none': 'text-secondary'    # Не отмечено - серый
    }
    return status_classes.get(status, 'text-secondary')

@register.filter
def get_attendance_status(attendance_dict, date):
    return attendance_dict.get(date, 'none')