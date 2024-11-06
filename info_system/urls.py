from django.urls import path
from . import views

urlpatterns = [
    path('attendance/', views.attendance_view, name='attendance'),
    path('api/attendance/update/', views.update_attendance, name='update_attendance'),
] 