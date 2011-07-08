""" This is the glue that links html views from wherever into email-able reports """

from logistics.views import reporting, aggregate
from email_reports.schedule import ReportSchedule

REPORTING_REPORT = ReportSchedule(reporting,
                                  title="Reporting Rates")
AGGREGATE_REPORT = ReportSchedule(aggregate,
                                  title="Aggregate Stock Report")

SCHEDULABLE_REPORTS = {
                       "aggregate": AGGREGATE_REPORT,
                       "reporting": REPORTING_REPORT,
                       }
