import random
import string

from django.contrib.auth.models import User
from django.test import TestCase

from email_reports.models import SchedulableReport, ReportSubscription


HTML_TEMPLATE = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
        <title>title</title>
    </head>
    <body>
        %(noise)s
        <div id='report-title'>%(title)s</div>
        %(noise)s
        <div id='report-content'>%(content)s</div>
        %(noise)s
    </body>
</html>
"""


class BaseReportTestCase(TestCase):
    "Common test case for creating test data."

    urls = 'email_reports.tests.urls'

    def get_random_string(self, length=10):
        "Create a random string."
        return u''.join(random.choice(string.ascii_letters) for x in xrange(length))

    def create_user(self, **kwargs):
        "Create a test user."
        info = {
            'username': self.get_random_string(),
            'password': self.get_random_string(),
            'email': ''
        }
        info.update(kwargs)
        return User.objects.create_user(**info)

    def create_report(self, **kwargs):
        "Create a test scheduleable report."
        info = {
            'view_name': 'test-report',
            'display_name': self.get_random_string(),
        }
        info.update(kwargs)
        return SchedulableReport.objects.create(**info)

    def create_report_subscription(self, **kwargs):
        "Create a test report ReportSubscription."
        info = {
            '_view_args': None,
        }
        info.update(kwargs)
        if 'report' not in info:
            info['report'] = self.create_report()
        return ReportSubscription.objects.create(**info)
