from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentUser, Mentor
from info_system.models import Attendance, Grade
from .decorators import mentor_required, student_required, manager_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from info_system.group_model import Group  # Импортируем нашу модель Group

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('manager_dashboard')
            elif hasattr(user, 'manager_profile'):
                return redirect('manager_dashboard')
            elif hasattr(user, 'mentor_profile'):
                return redirect('mentor_dashboard')
            elif hasattr(user, 'student_profile'):
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Неверный тип пользователя')
                return redirect('login')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'auth_app/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def main_page(request):
    if hasattr(request.user, 'mentor_profile'):
        return redirect('mentor_dashboard')
    return render(request, 'auth_app/main_page.html')

@login_required
def mentor_dashboard(request):
    mentor = request.user.mentor_profile
    groups = mentor.groups.all()
    return render(request, 'auth_app/mentor/dashboard.html', {'groups': groups})

@login_required
def mentor_groups(request):
    mentor = request.user.mentor_profile
    groups = mentor.groups.all()
    return render(request, 'auth_app/mentor/groups.html', {'groups': groups})

@login_required
def mentor_students(request):
    mentor = request.user.mentor_profile
    group_id = request.GET.get('group')
    
    if group_id:
        students = StudentUser.objects.filter(group__in=mentor.mentored_groups.all(), group_id=group_id)
    else:
        students = StudentUser.objects.filter(group__in=mentor.mentored_groups.all())
    
    return render(request, 'auth_app/mentor/students.html', {'students': students})

@student_required
def student_profile(request):
    student = request.user.student_profile
    return render(request, 'auth_app/student/profile.html', {'student': student})

@student_required
def student_grades(request):
    student = request.user.student_profile
    return render(request, 'auth_app/student/grades.html', {'student': student})

@student_required
def student_progress(request):
    student = request.user.student_profile
    return render(request, 'auth_app/student/progress.html', {'student': student})

@login_required
@student_required
def student_dashboard(request):
    student = request.user.student_profile
    context = {
        'student': student
    }
    return render(request, 'auth_app/student/dashboard.html', context)

def is_manager(user):
    return hasattr(user, 'manager_profile')

@user_passes_test(is_manager)
def update_student_status(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(StudentUser, id=student_id)
        new_status = request.POST.get('payment_status')
        if new_status in dict(StudentUser.PAYMENT_STATUS_CHOICES):
            student.payment_status = new_status
            student.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@user_passes_test(is_manager)
def update_mentor_status(request, mentor_id):
    if request.method == 'POST':
        mentor = get_object_or_404(Mentor, id=mentor_id)
        new_status = request.POST.get('report_status')
        if new_status in dict(Mentor.REPORT_STATUS_CHOICES):
            mentor.report_status = new_status
            mentor.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
@manager_required
def manager_dashboard(request):
    mentors = Mentor.objects.all()
    groups = Group.objects.all()
    students_count = StudentUser.objects.all().count()
    mentors_count = mentors.count()
    
    context = {
        'groups': groups,
        'students_count': students_count,
        'mentors_count': mentors_count
    }
    return render(request, 'auth_app/manager/dashboard.html', context)

@login_required
@manager_required
def manage_students(request):
    students = StudentUser.objects.all()
    return render(request, 'auth_app/manager/students.html', {'students': students})

@login_required
@manager_required
def manage_mentors(request):
    mentors = Mentor.objects.all()
    return render(request, 'auth_app/manager/mentors.html', {'mentors': mentors})

@login_required
@mentor_required
def update_attendance(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(StudentUser, id=student_id)
        lesson_id = request.POST.get('lesson_id')
        date = request.POST.get('date')
        status = request.POST.get('status')
        
        if student.group in request.user.mentor_profile.groups.all():
            attendance, created = Attendance.objects.update_or_create(
                student=student,
                lesson_id=lesson_id,
                date=date,
                defaults={'status': status}
            )
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403)

@login_required
@mentor_required
def update_grades(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(StudentUser, id=student_id)
        if student.group in request.user.mentor_profile.assigned_groups.all():
            grade = Grade.objects.get(student=student)
            grade.behaviour = request.POST.get('behaviour')
            grade.motivation = request.POST.get('motivation')
            grade.grade_level = request.POST.get('grade_level')
            grade.activities = request.POST.get('activities')
            grade.attendance = request.POST.get('attendance')
            grade.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403)

@login_required
@manager_required
def update_student_payment(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(StudentUser, id=student_id)
        new_status = request.POST.get('payment_status')
        if new_status in dict(StudentUser.PAYMENT_STATUS_CHOICES):
            student.payment_status = new_status
            student.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
@manager_required
def update_mentor_report(request, mentor_id):
    if request.method == 'POST':
        mentor = get_object_or_404(Mentor, id=mentor_id)
        new_status = request.POST.get('report_status')
        if new_status in dict(Mentor.REPORT_STATUS_CHOICES):
            mentor.report_status = new_status
            mentor.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@manager_required
def manage_groups(request):
    groups = Group.objects.all()
    return render(request, 'auth_app/manager/groups.html', {'groups': groups})
@manager_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    students = StudentUser.objects.filter(group=group)
    
    context = {
        'group': group,
        'students': students,
    }
    return render(request, 'auth_app/manager/group_detail.html', context)

@login_required
@student_required
def student_achievements(request):
    student = request.user.student_profile
    achievements = student.student_achievements.all()
    context = {
        'student': student,
        'achievements': achievements
    }
    return render(request, 'auth_app/student/achievements.html', context)

@login_required
@student_required
def student_grades(request):
    student = request.user.student_profile
    grade = Grade.objects.get_or_create(student=student)[0]
    context = {
        'student': student,
        'grade': grade
    }
    return render(request, 'auth_app/student/grades.html', context)

@login_required
@student_required
def student_group_info(request):
    student = request.user.student_profile
    context = {
        'student': student,
        'group': student.group
    }
    return render(request, 'auth_app/student/group_info.html', context)

@mentor_required
def student_detail(request, student_id):
    student = get_object_or_404(StudentUser, id=student_id)
    # Проверяем, что студент принадлежит к группе ментора
    if student.group not in request.user.mentor_profile.groups.all():
        return HttpResponseForbidden()
    
    context = {
        'student': student,
    }
    return render(request, 'auth_app/mentor/student_detail.html', context)