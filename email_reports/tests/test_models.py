"Test model methods."

from django.core import mail

from email_reports.models import SchedulableReport
from email_reports.tests.base import BaseReportTestCase


class SendHTMLReportTestCase(BaseReportTestCase):
    "Send HTML email by parsing view reponse HTML."

    def setUp(self):
        self.report = self.create_report(view_name='test-report', report_type=SchedulableReport.TYPE_HTML)
        self.subscription = self.create_report_subscription(report=self.report)
        self.user = self.create_user()
        self.subscription.users.add(self.user)

    def test_send_single_email(self):
        "Parse email body to send to the users."
        self.subscription.send()
        self.assertEqual(len(mail.outbox), 1)
