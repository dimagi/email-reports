email-reports
===============

Take any django view and email it out as a pdf on a daily or weekly basis
* UI for users can add or remove any email report 
* UI for users to test sending of email report

Installation
===============

0. Install wkhtmltopdf*
1. Install app and link urls like you would any other django app. Update the MAGIC TOKEN in your settings.py
2. Register any view name that you want to be able to send out via pdf over email in the SchedulableReport model. You'll also need to add the magic_token_required decorator to those views so that the scheduler task can hit them.
3. Make sure that your view prints nicely, taking advantage of the css 'media=print' option
4. Ensure that logins can be circumvented with the use of the MAGIC TOKEN in settings.py

And that's it.


*When running in daemon mode, you may need to set up a dummy x server in order to use wkhtmltopdf. 
Here are some instructions, modified from http://drupal.org/node/870058

1. apt-get install wkhtmltopdf
4. Install required support packages. sudo apt-get install openssl build-essential xorg libssl-dev
5. Check to see if it works: run wkhtmltopdf http://www.google.com test.pdf. If it works, then you are done -- make sure to make a symbolic link as per INSTRUCTIONS.txt. If you get the error "Cannot connect to X server" then continue to number 6.
6. We need to run it headless on a 'virtual' x server. We will do this with a package called xvfb. sudo apt-get install xvfb
7. We need to write a little shell script to wrap wkhtmltopdf in xvfb. Make a file called wkhtmltopdf.sh and add the following:
xvfb-run -a -s "-screen 0 640x480x16" wkhtmltopdf $*
8. Move this shell script to /usr/bin, and set permissions: sudo chmod a+x /usr/bin/wkhtmltopdf.sh
Call wkhtmltopdf.sh instead of wkhtmltopdf
