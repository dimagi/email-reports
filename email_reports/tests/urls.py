"URL patterns for views using in the test cases."
from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns('email_reports.tests.views',
    url(r'^reports/', include('email_reports.urls')),
    url(r'^test/report/$', 'report', name='test-report'),
)

