from rapidsms.tests.scripted import TestScript
from email_reports.tasks import *

class TestReports (TestScript):
    def testDailyEmailReports(self):
        daily_reports()

    def testWeeklyEmailReports(self):
        weekly_reports()

    def testMonthlyEmailReports(self):
        monthly_reports()
