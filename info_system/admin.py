from django.contrib import admin
from .models import Grade, Progress, Attendance, Achievement
from .group_model import Group, LessonSchedule

class LessonScheduleInline(admin.TabularInline):
    model = LessonSchedule
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    inlines = [LessonScheduleInline]
    # TODO: Раскомментировать после добавления приложения code_tester
    # filter_horizontal = ('coding_tasks',)

class GradeAdmin(admin.ModelAdmin):
    list_display = ('get_student_name', 'behaviour', 'motivation', 'grade_level', 'activities', 'attendance', 'is_present', 'average_grade')

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    get_student_name.short_description = 'Student'

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'date', 'status')
    list_filter = ('lesson__group', 'date', 'status')
    search_fields = ('student__first_name', 'student__last_name', 'lesson__group__name')

admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Progress)
admin.site.register(Group, GroupAdmin)
admin.site.register(Achievement)