"Test model methods."

from mock import patch

from .base import BaseReportTestCase
from email_reports.models import SchedulableReport


class SendHTMLReportTestCase(BaseReportTestCase):
    "Send HTML email by parsing view reponse HTML."

    def setUp(self):
        self.report = self.create_report(view_name='test-report', report_type=SchedulableReport.TYPE_HTML)
        self.subscription = self.create_report_subscription(report=self.report)
        self.user = self.create_user()
        self.subscription.users.add(self.user)

    def test_send_single_email(self):
        "Parse email body to send to the users."
        with patch('email_reports.models.send_HTML_email') as send_email:
            self.subscription.send()
            self.assertEqual(send_email.call_count, 1)
            args, kwargs = send_email.call_args
            title, email, body = args           
            self.assertEqual(email, self.user.email)
            # Email subject uses report display name by default
            self.assertTrue(self.report.display_name in title)
