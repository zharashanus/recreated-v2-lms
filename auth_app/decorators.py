from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def manager_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and (hasattr(request.user, 'manager_profile') or request.user.is_superuser):
            return function(request, *args, **kwargs)
        return redirect('login')
    return wrap

def mentor_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'mentor_profile'):
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrap

def student_required(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, 'student_profile'):
            return function(request, *args, **kwargs)
        return redirect('login')
    return wrap