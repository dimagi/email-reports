"URL patterns for views using in the test cases."
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('email_reports.tests.views'
    url(r'^test/report/$', 'report', name='test-report'),
)

