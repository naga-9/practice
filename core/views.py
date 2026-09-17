import time

from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import Contact
from .unpoly import up_validate


def home(request):
    return render(request, "core/home.html")


def about(request):
    return render(request, "core/about.html")


def fragments(request):
    # ?slow=<seconds> delays the response so Unpoly's loading states are visible on localhost.
    if request.GET.get("slow"):
        time.sleep(min(float(request.GET["slow"]), 10))
    return render(request, "core/fragments.html")


def contacts(request):
    """List of contacts plus a create form, all on one page."""
    status = 200
    if request.method == "POST":
        form = ContactForm(request.POST)
        if up_validate(request):
            # [up-validate]: run validation and re-render, but never save.
            form.is_valid()
        elif form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your message was saved.")
            # Post/Redirect/Get. Unpoly follows the redirect and renders the target from it.
            return redirect("contacts")
        else:
            # Unpoly treats 2xx as success and would render into the success target.
            # A 422 tells it the submission failed, so it renders [up-fail-target] instead.
            status = 422
    else:
        form = ContactForm()

    context = {"form": form, "contacts": Contact.objects.all()}
    return render(request, "core/contacts.html", context, status=status)
