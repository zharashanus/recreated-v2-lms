from django.contrib import admin
from .models import Grade, Progress, Attendance, Achievement
from .group_model import Group, LessonSchedule
# TODO: Раскомментировать после добавления приложения code_tester
# from code_tester.models import CodingTask

class LessonScheduleInline(admin.TabularInline):
    model = LessonSchedule
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    inlines = [LessonScheduleInline]
    # TODO: Раскомментировать после добавления приложения code_tester
    # filter_horizontal = ('coding_tasks',)
    
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == "coding_tasks":
    #         kwargs["queryset"] = CodingTask.objects.all().order_by('title')
    #     return super().formfield_for_manytomany(db_field, request, **kwargs)

class GradeAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'behaviour', 'motivation', 'grade_level', 'activities', 'attendance', 'is_present', 'average_grade')

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    get_student_name.short_description = 'Student'

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'get_schedule', 'date', 'status']
    list_filter = ['student__group', 'date', 'status']
    search_fields = ['student__first_name', 'student__last_name']

    def get_schedule(self, obj):
        return obj.lesson.schedule if obj.lesson else '-'
    get_schedule.short_description = 'Schedule'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('attendance-view/', self.admin_site.admin_view(self.attendance_view),
                 name='attendance-view'),
        ]
        return custom_urls + urls

    def attendance_view(self, request):
        from django.shortcuts import render
        from datetime import datetime
        from calendar import monthrange
        from dateutil.relativedelta import relativedelta
        
        context = dict(
            self.admin_site.each_context(request),
            groups=Group.objects.all(),
            title='Управление посещаемостью'
        )
        
        selected_group_id = request.GET.get('group')
        if selected_group_id:
            group = Group.objects.get(id=selected_group_id)
            current_date = datetime.now()
            month = int(request.GET.get('month', current_date.month))
            year = int(request.GET.get('year', current_date.year))
            
            selected_date = datetime(year, month, 1)
            _, last_day = monthrange(year, month)
            
            context.update({
                'selected_group': group,
                'students': group.students.all(),
                'current_month': selected_date,
                'prev_month': selected_date - relativedelta(months=1),
                'next_month': selected_date + relativedelta(months=1),
                'attendance_data': self.get_attendance_data(group, selected_date, last_day)
            })
        
        return render(request, 'admin/info_system/attendance/attendance_view.html', context)

    def get_attendance_data(self, group, start_date, last_day):
        from datetime import timedelta
        
        end_date = start_date.replace(day=last_day)
        students = group.students.all()
        schedules = group.lesson_schedules.filter(is_active=True)
        
        attendance_data = {}
        for student in students:
            attendance_data[student] = {}
            current_date = start_date
            while current_date <= end_date:
                for schedule in schedules:
                    if schedule.day_of_week == current_date.weekday():
                        attendance = Attendance.objects.get_or_create(
                            student=student,
                            schedule=schedule,
                            date=current_date
                        )[0]
                        attendance_data[student][current_date] = attendance
                current_date += timedelta(days=1)
        
        return attendance_data

admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Progress)
admin.site.register(Group, GroupAdmin)
admin.site.register(Achievement)