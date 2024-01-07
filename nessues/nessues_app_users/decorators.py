from django.shortcuts import redirect
from django.http import HttpResponse


def authenticated(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return view_function(request, *args, **kwargs)
    return wrapper_function


def unauthenticated(view_function):
    def wrapper_function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        return view_function(request, *args, **kwargs)
    return wrapper_function