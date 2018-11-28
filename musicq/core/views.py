from django.shortcuts import render, get_object_or_404


def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')
