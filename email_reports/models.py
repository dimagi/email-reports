""" These models define user's subscriptions to reports specified in schedule/config.py """

#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import os, subprocess
import json
import tempfile
from subprocess import PIPE
from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from rapidsms.conf import settings
from dimagi.utils.django.email import send_HTML_email
from dimagi.utils.mixins import UnicodeMixIn
from email_reports.schedule import ReportSchedule


class SchedulableReport(models.Model):
    """ can turns django views into emailable html reports """
    
    TYPE_PDF = 1
    TYPE_HTML = 2

    TYPE_CHOICES = (
        (TYPE_PDF, 'PDF'),
        (TYPE_HTML, 'HTML'),
    )

    # names of django views which can be pdf-ified and 
    # sent out regularly over email
    view_name = models.CharField(max_length=100)
    # name to display on the 'add report' page
    # note that the reports themselves will be emailed using 
    # the html.head.title element of the view
    display_name = models.CharField(max_length=255)
    report_type = models.IntegerField(choices=TYPE_CHOICES, default=TYPE_PDF)

    def __unicode__(self):
        return self.view_name

    def email_subject(self, user, view_args={}):
        try:
            site = Site.objects.get().name
        except Site.DoesNotExist:
            site = 'RapidSMS' # or whatever
        return "%(site)s Report: %(report)s" % {'site': site, 
                                                'report':self.display_name }
    
    def get_path_to_pdf(self, user, view_args={}):
        urlbase = Site.objects.get_current().domain
        # TODO: add view args back
        full_url='%(base)s%(path)s?magic_token=%(token)s' % \
                 {"base": urlbase, "path": reverse(self.view_name, kwargs=view_args), 
                  "token": settings.MAGIC_TOKEN}
        fd, tmpfilepath = tempfile.mkstemp(suffix=".pdf", prefix="%s-report-" % self.view_name)
        os.close(fd)
        command = 'wkhtmltopdf.sh --print-media-type --use-xserver "%(url)s" %(file)s' % \
                  {"url": full_url, "file": tmpfilepath}
        p = subprocess.Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        p.communicate()
        return tmpfilepath

class ReportSubscription(models.Model, UnicodeMixIn):
    report = models.ForeignKey(SchedulableReport)
    _view_args = models.CharField(max_length=512, null=True, blank=True)
    users = models.ManyToManyField(User)
    
    def __unicode__(self):
        return "Notify: %s user(s): %s, report: %s" % \
                (self.__class__.__name__, ",".\
                 join([u.username for u in self.users.all()]), 
                 self.report)

    def send(self):
        func = lambda x: None
        if self.report.report_type == SchedulableReport.TYPE_PDF:
            func = self.send_pdf_to_user
        elif self.report.report_type == SchedulableReport.TYPE_HTML:
            func = self.send_html_to_user
        for user in self.users.all():
            func(user)
    
    def send_pdf_to_user(self, user):
        report = self.report.get_path_to_pdf(user, self.view_args)
        title = self.report.email_subject(user, self.view_args)
        email = EmailMessage(title, 'See attachment',
                             settings.EMAIL_LOGIN, [user.email])
        email.attach_file(report)
        email.send(fail_silently=False)
    
    def send_html_to_user(self, user):
        # because we could have html-email reports (using report-body div's) live alongside
        # pdf reports, i've left this code as is
        url = reverse(self.report.view_name, kwargs=self.view_args)
        func, args, kwargs = resolve(url)
        report = ReportSchedule(func, title=self.report.display_name)
        body = report.get_response(user, self.view_args)
        title = report.title
        try:
            site_name = Site.objects.get().name
        except Site.DoesNotExist:
            pass
        else:
            title = "{0} {1}".format(site_name, title)
        send_HTML_email(title, user.email, body)

    @property
    def view_args(self):
        if self._view_args:
            return json.loads(self._view_args)
        return self._view_args or {}

    @view_args.setter
    def view_args(self, value):
        self._view_args = json.dumps(value)

    @view_args.deleter
    def view_args(self):
        self._view_args = None

class DailyReportSubscription(ReportSubscription):
    # removing these, since they break navigation in django admin
    #__name__ = "DailyReportNotification"    
    hours = models.IntegerField()

class WeeklyReportSubscription(ReportSubscription):
    # removing these, since they break navigation in django admin
    #__name__ = "WeeklyReportNotification"
    hours = models.IntegerField()
    day_of_week = models.IntegerField()

