"""Minimal helpers for Unpoly's X-Up-* request headers."""


def is_unpoly(request):
    """True when the request was made by Unpoly (any X-Up-* header present)."""
    return "X-Up-Version" in request.headers


def up_target(request):
    """The CSS selector Unpoly wants updated, or None for a normal request."""
    return request.headers.get("X-Up-Target")


def up_validate(request):
    """
    Names of the fields being validated via [up-validate], or None.

    Unpoly submits the form with X-Up-Validate set when a watched field changes.
    The server should validate and re-render the form *without* saving.
    """
    return request.headers.get("X-Up-Validate")


def base_template(request):
    """
    Template that page templates should extend.

    For Unpoly fragment requests we skip the full layout (head, nav) and return only
    the <main> element, since that's all Unpoly is going to use.
    """
    return "partial.html" if up_target(request) else "layout.html"
