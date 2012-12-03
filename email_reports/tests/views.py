from django.http import HttpResponse

from .base import HTML_TEMPLATE


def report(request):
    "Minimal HTML report response."
    html = HTML_TEMPLATE % {'title': 'Foo', 'content': 'Bar', 'noise': ''}
    return HttpResponse(content=html)
