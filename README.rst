email-reports
===============

Take any django view and email it out as a pdf on a daily or weekly basis
* UI for users can add or remove any email report 
* UI for users to test sending of email report

Installation
===============

0. Install app and link urls like you would any other django app. Update the MAGIC TOKEN in your settings.py
1. Register any view name that you want to be able to send out via pdf over email in the SchedulableReport model
2. Make sure that your view prints nicely, taking advantage of the css 'media=print' option
3. Ensure that logins can be circumvented with the use of the MAGIC TOKEN in settings.py

And that's it.

