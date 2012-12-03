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

    def test_parse_title_html(self):
        "Parse title from report-title div when that div contains HTML."
        title = "<h1>This is my title</h1>"
        html = HTML_TEMPLATE % {'title': title, 'content': 'Bar', 'noise': ''}
        parser = ReportParser(html)
        self.assertEqual(parser.title, title)

    def test_parse_content_html(self):
        "Parse body from report-content div when that div contains HTML."
        content = "<p>Lorem Ipsum</p>"
        html = HTML_TEMPLATE % {'title': 'Foo', 'content': content, 'noise': ''}
        parser = ReportParser(html)
        self.assertEqual(parser.body, content)

    def test_parse_title_messy(self):
        "Parse title from report-title div with surrounding messy HTML."
        noise = '<div>' * 100
        html = HTML_TEMPLATE % {'title': 'Foo', 'content': 'Bar', 'noise': noise}
        parser = ReportParser(html)
        self.assertEqual(parser.title, 'Foo')

    def test_parse_content_messy(self):
        "Parse body from report-content div with surrounding messy HTML."
        noise = '<div>' * 100
        html = HTML_TEMPLATE % {'title': 'Foo', 'content': 'Bar', 'noise': noise}
        parser = ReportParser(html)
        self.assertEqual(parser.body, 'Bar')

    def test_parse_title_non_found(self):
        "Return None if title is not found."
        html = '<html></html>'
        parser = ReportParser(html)
        self.assertEqual(parser.title, None)

    def test_parse_content_non_found(self):
        "Return None if content is not found."
        html = '<html></html>'
        parser = ReportParser(html)
        self.assertEqual(parser.body, None)
