import unittest

from .base import HTML_TEMPLATE
from email_reports.schedule.parsers import ReportParser


class ReportParserTestCase(unittest.TestCase):
    "Parse report title and content from HTML by id."

    def test_parse_title_simple(self):
        "Parse title from report-title div."
        html = HTML_TEMPLATE % {'title': 'Foo', 'content': 'Bar', 'noise': ''}
        parser = ReportParser(html)
        self.assertEqual(parser.title, 'Foo')

    def test_parse_content_simple(self):
        "Parse body from report-content div."
        html = HTML_TEMPLATE % {'title': 'Foo', 'content': 'Bar', 'noise': ''}
        parser = ReportParser(html)
        self.assertEqual(parser.body, 'Bar')

    def test_parse_title_noisy(self):
        "Parse title from report-title div with surrounding noise."
        noise = '<span></span>' * 100
        html = HTML_TEMPLATE % {'title': 'Foo', 'content': 'Bar', 'noise': noise}
        parser = ReportParser(html)
        self.assertEqual(parser.title, 'Foo')

    def test_parse_content_noisy(self):
        "Parse body from report-content div with surrounding noise."
        noise = '<span></span>' * 100
        html = HTML_TEMPLATE % {'title': 'Foo', 'content': 'Bar', 'noise': noise}
        parser = ReportParser(html)
        self.assertEqual(parser.body, 'Bar')
