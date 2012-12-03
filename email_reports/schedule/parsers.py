""" This parser allows you to take any html report with a <div 
id='report-title'>title</div> and a <div id='report-content'>
content</div> and spew out just the part of the report in
report-title and report-content"""

from xml.etree import ElementTree

from html5lib import HTMLParser, treebuilders


class ReportParser():
    def __init__(self, raw_html):
        parser = HTMLParser(tree=treebuilders.getTreeBuilder("etree"),
            namespaceHTMLElements=False)
        self._doc = parser.parse(raw_html)
        self._divs = {}
        for div in self._doc.findall('body//div'):
            if 'id' in div.attrib:
                text = div.text or u''
                children = u''.join(map(ElementTree.tostring, div))
                self._divs[div.attrib['id']] = u'%s%s' % (text, children)

    @property
    def title(self):
        return self._divs.get('report-title')

    @property
    def body(self):
        return self._divs.get('report-content')
        
    def get_html(self):
        return "%(title)s\n%(body)s" % {"title": self.title, "body": self.body}
