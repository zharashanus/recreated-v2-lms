from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [reverse('login'), '/admin/', '/static/', 'next']

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            if not any(url in path for url in self.exempt_urls):
                return redirect('login')
        return self.get_response(request)