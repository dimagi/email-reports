#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.contrib import admin
from email_reports.models import *

class WeeklyReportSubscriptionAdmin(admin.ModelAdmin):
    model = WeeklyReportSubscription

class DailyReportSubscriptionAdmin(admin.ModelAdmin):
    model = DailyReportSubscription

class SchedulableReportAdmin(admin.ModelAdmin):
    model = SchedulableReport

admin.site.register(WeeklyReportSubscription, WeeklyReportSubscriptionAdmin)
admin.site.register(DailyReportSubscription, DailyReportSubscriptionAdmin)
admin.site.register(SchedulableReport, SchedulableReportAdmin)

