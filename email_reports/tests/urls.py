"URL patterns for views using in the test cases."
from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns('email_reports.tests.views',
    url(r'^reports/', include('email_reports.urls')),
    url(r'^test/report/$', 'report', name='test-report'),
    url(r'^test/report/(?P<report_id>\d+)/$', 'report_with_arg', name='test-report-id'),
    url(r'^test/report/subject/$', 'report_with_subject', name='test-report-subject'),
)

