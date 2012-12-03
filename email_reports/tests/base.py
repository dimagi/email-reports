import random
import string

from django.contrib.auth.models import User
from django.test import TestCase

from email_reports.models import SchedulableReport, ReportSubscription


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
