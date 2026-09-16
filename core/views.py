import time

from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")


def fragments(request):
    # ?slow=<seconds> delays the response so Unpoly's loading states are visible on localhost.
    if request.GET.get("slow"):
        time.sleep(min(float(request.GET["slow"]), 10))
    return render(request, "core/fragments.html")
