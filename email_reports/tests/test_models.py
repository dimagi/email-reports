"Test model methods."

import json

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

    def test_send_multiple_emails(self):
        "Parse email body to send to the all users."
        other_user = self.create_user()
        self.subscription.users.add(other_user)
        with patch('email_reports.models.send_HTML_email') as send_email:
            self.subscription.send()
            self.assertEqual(send_email.call_count, 2)

    def test_email_subject(self):
        "Title is generated from report display name."
        with patch('email_reports.models.send_HTML_email') as send_email:
            self.subscription.send()
            args, kwargs = send_email.call_args
            title, email, body = args           
            self.assertTrue(self.report.display_name in title)

    def test_email_body(self):
        "Body should be parsed from view content."
        with patch('email_reports.models.send_HTML_email') as send_email:
            self.subscription.send()
            args, kwargs = send_email.call_args
            title, email, body = args
            # Default body content           
            self.assertTrue('Bar' in body)

    def test_view_args(self):
        "Subscription can be saved with serialized arguments for the view."        
        self.report.view_name = 'test-report-id'
        self.report.save()
        args = {'report_id': 100}
        self.subscription._view_args = json.dumps(args)
        self.subscription.save()
        with patch('email_reports.models.send_HTML_email') as send_email:
            self.subscription.send()
            args, kwargs = send_email.call_args
            title, email, body = args  
            self.assertTrue('Report ID: 100' in body)

    def test_email_subject_parsed(self):
        "Subject can be optionally parsed from the HTML. New lines are removed."
        self.report.view_name = 'test-report-subject'
        self.report.save()
        with patch('email_reports.models.send_HTML_email') as send_email:
            self.subscription.send()
            args, kwargs = send_email.call_args
            title, email, body = args
            self.assertEqual(title, "Custom Subject")
