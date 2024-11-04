from django.contrib import admin
from .models import StudentUser, Mentor, Manager

class StudentUserAdmin(admin.ModelAdmin):
    list_display = ('avatar_tag', 'first_name', 'last_name', 'age', 'group', 'payment_status')
    list_filter = ('group', 'payment_status')
    search_fields = ('first_name', 'last_name')

class MentorAdmin(admin.ModelAdmin):
    list_display = ('avatar_tag', 'first_name', 'last_name', 'specialization', 'experience_years', 'report_status')
    list_filter = ('specialization', 'report_status')
    search_fields = ('first_name', 'last_name', 'specialization')

class ManagerAdmin(admin.ModelAdmin):
    list_display = ('avatar_tag', 'first_name', 'last_name', 'specialization', 'experience')
    search_fields = ('first_name', 'last_name', 'specialization')

admin.site.register(StudentUser, StudentUserAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Manager, ManagerAdmin) 