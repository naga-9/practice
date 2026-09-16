from django.utils import timezone

from .unpoly import base_template


def unpoly(request):
    """Expose the Unpoly-aware base template (and a timestamp for demos) to every template."""
    return {
        "base_template": base_template(request),
        "now": timezone.localtime(),
    }
