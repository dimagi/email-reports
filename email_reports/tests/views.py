from django.http import HttpResponse

from .base import HTML_TEMPLATE


def report(request):
    "Minimal HTML report response."
    html = HTML_TEMPLATE % {'title': 'Foo', 'content': 'Bar', 'noise': ''}
    return HttpResponse(content=html)


def report_with_arg(request, report_id):
    "Minimal HTML report response."
    html = HTML_TEMPLATE % {'title': 'Report with Arg', 'content': 'Report ID: %s' % report_id, 'noise': ''}
    return HttpResponse(content=html)

def report_with_subject(request):
    "Include an email subject in the HTML report response."
    content = "<div id='report-subject'>Custom \nSubject</div>"
    html = HTML_TEMPLATE % {'title': 'Report with Subject', 'content': content, 'noise': ''}
    return HttpResponse(content=html)
