import calendar
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rapidsms.contrib.locations.models import Location
from dimagi.utils.web import render_to_response
from email_reports.models import ReportSubscription, \
    DailyReportSubscription, WeeklyReportSubscription, \
    SchedulableReport

@login_required
def email_reports(request, pk=None, context={}, template="reports/scheduled_reports.html"):
    context['user'] = request.user
    if pk is not None:
        context['user'] = get_object_or_404(User, pk=pk)
    d = [d for d in DailyReportSubscription.objects.filter(users=context['user'])]
    w = [w for w in WeeklyReportSubscription.objects.filter(users=context['user'])]
    context['scheduled_reports'] = d + w
    return render_to_response(
        request, template, context
    )

def add_scheduled_report(request, user_id):
    recipient = User.objects.get(pk=user_id)
    if request.method == "POST":
        report_id = request.POST["report_id"]
        hour = request.POST["hour"]
        day = request.POST["day"]
        if day=="all":
            report = DailyReportSubscription()
        else:
            report = WeeklyReportSubscription()
            report.day_of_week = int(day)
        report.hours = int(hour)
        report.report = SchedulableReport.objects.get(pk=report_id)
        # not generic
        location_code = request.POST["location_code"]
        report.view_args = {'location_code':location_code}

        report.save()
        report.users.add(recipient)
        report.save()
        messages.success(request, "New scheduled report added!")
        return HttpResponseRedirect(reverse("email_reports"))
    context = {}
    context.update({"hours": [(val, "%s:00" % val) for val in range(24)],
                    "days":  [(val, calendar.day_name[val]) for val in range(7)],
                    "reports": SchedulableReport.objects.all()})
    # here we get less generic : b
    context['locations'] = Location.objects.all()
    context['recipient'] = recipient
    return render_to_response(request, "reports/add_scheduled_report.html", context)

#@require_POST
def drop_scheduled_report(request, user_id, report_id):
    report = ReportSubscription.objects.get(pk=report_id)
    try:
        user = User.objects.get(pk=user_id)
        report.users.remove(user)
    except ValueError:
        pass # odd, the user wasn't there in the first place
    if report.users.count() == 0:
        report.delete()
    else:
        report.save()
    messages.success(request, "Scheduled report dropped!")
    return HttpResponseRedirect(reverse("email_reports"))

#@require_POST
def test_scheduled_report(request, user_id, report_id):
    report = ReportSubscription.objects.get(pk=report_id)
    user = User.objects.get(pk=user_id)
    report.send_pdf_to_user(user)
    messages.success(request, "Test message sent to %s" % user.email)
    return HttpResponseRedirect(reverse("email_reports"))
