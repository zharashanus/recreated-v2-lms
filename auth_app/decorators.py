from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def manager_required(function):
    def check_manager(user):
        return hasattr(user, 'manager_profile')
    
    decorated_function = user_passes_test(check_manager)(function)
    return decorated_function

def mentor_required(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, 'mentor_profile'):
            return function(request, *args, **kwargs)
        return redirect('login')
    return wrap

def student_required(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, 'student_profile'):
            return function(request, *args, **kwargs)
        return redirect('login')
    return wrap