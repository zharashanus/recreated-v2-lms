from django.urls import path
from . import views
from info_system.views import attendance_view, update_attendance

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Manager URLs
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/students/', views.manage_students, name='manage_students'),
    path('manager/mentors/', views.manage_mentors, name='manage_mentors'),
    path('manager/student/<int:student_id>/update-payment/', views.update_student_payment, name='update_student_payment'),
    path('manager/mentor/<int:mentor_id>/update-report/', views.update_mentor_report, name='update_mentor_report'),
    path('manager/groups/', views.manage_groups, name='manage_groups'),
    path('manager/group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('manager/attendance/', attendance_view, name='manager_attendance'),
    path('manager/update-attendance/', update_attendance, name='manager_update_attendance'),
    
    # Mentor URLs
    path('mentor/dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    path('mentor/attendance/', attendance_view, name='mentor_attendance'),
    path('mentor/update-attendance/', update_attendance, name='mentor_update_attendance'),
    path('mentor/grades/<int:student_id>/', views.update_grades, name='update_grades'),
    path('mentor/groups/', views.mentor_groups, name='mentor_groups'),
    path('mentor/students/', views.mentor_students, name='mentor_students'),
    path('mentor/student/<int:student_id>/', views.student_detail, name='student_detail'),
    
    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.student_profile, name='student_profile'),
    path('student/grades/', views.student_grades, name='student_grades'),
    path('student/progress/', views.student_progress, name='student_progress'),
    path('student/achievements/', views.student_achievements, name='student_achievements'),
    path('student/group/', views.student_group_info, name='student_group_info'),
]