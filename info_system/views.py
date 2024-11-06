from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from .models import Group, LessonSchedule, Attendance
from auth_app.models import StudentUser
from django.template.defaulttags import register
from django.views.decorators.http import require_POST
import json
from django.views.generic import TemplateView

@login_required
def attendance_view(request):
    template_name = 'info_system/attendance.html'
    
    # Добавим отладочную информацию
    print("Debug: Starting attendance_view")
    
    if hasattr(request.user, 'mentor'):
        groups = request.user.mentor.groups.all()
    else:
        groups = Group.objects.all()
    
    print(f"Debug: Found {groups.count()} groups")
    
    context = {
        'groups': groups,
        'students': StudentUser.objects.none()
    }
    
    # Get current month dates
    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    
    month_start = date(year, month, 1)
    month_end = date(year, month, monthrange(year, month)[1])
    
    # Get selected group
    selected_group_id = request.GET.get('group')
    print(f"Debug: Selected group ID: {selected_group_id}")
    
    if selected_group_id:
        group = get_object_or_404(Group, id=selected_group_id)
        students = StudentUser.objects.filter(group=group)
        print(f"Debug: Found {students.count()} students in group")
        
        schedules = group.lesson_schedules.filter(is_active=True)
        print(f"Debug: Found {schedules.count()} schedules")
        
        dates_with_schedule = []
        students_attendance = []
        
        # Получаем даты
        current = month_start
        while current <= month_end:
            weekday = current.weekday()
            day_schedules = schedules.filter(day_of_week=weekday)
            for schedule in day_schedules:
                dates_with_schedule.append({
                    'date': current,
                    'lesson': schedule,
                    'weekday_name': schedule.get_day_of_week_display(),
                    'time': f"{schedule.start_time.strftime('%H:%M')}-{schedule.end_time.strftime('%H:%M')}"
                })
            current += timedelta(days=1)
        
        print(f"Debug: Generated {len(dates_with_schedule)} dates with schedule")
        
        # Формируем данные посещаемости
        for student in students:
            attendance_records = {}
            for date_info in dates_with_schedule:
                attendance = Attendance.objects.filter(
                    student=student,
                    lesson=date_info['lesson'],
                    date=date_info['date']
                ).first()
                attendance_records[date_info['date']] = attendance.status if attendance else 'none'
            
            students_attendance.append({
                'student': student,
                'attendance': attendance_records
            })
        
        print(f"Debug: Generated attendance data for {len(students_attendance)} students")
        
        context.update({
            'selected_group': group,
            'students': students,
            'dates_with_schedule': dates_with_schedule,
            'students_attendance': students_attendance,
            'prev_month': month_start - relativedelta(months=1),
            'next_month': month_start + relativedelta(months=1),
            'current_month': month_start,
            'today': date.today()
        })
    
    return render(request, template_name, context)

@require_POST
def update_attendance(request):
    data = json.loads(request.body)
    student_id = data.get('student_id')
    schedule_id = data.get('schedule_id')
    date = data.get('date')
    status = data.get('status')
    
    try:
        attendance, created = Attendance.objects.update_or_create(
            student_id=student_id,
            schedule_id=schedule_id,
            date=date,
            defaults={'status': status}
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
