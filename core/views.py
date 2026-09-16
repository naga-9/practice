from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")


def fragments(request):
    return render(request, "core/fragments.html")
