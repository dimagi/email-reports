DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django_nose',
    'djtables',
    'rapidsms',
    'rapidsms.contrib.locations',
    'rapidsms.contrib.messagelog',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'djcelery',
    'logistics',
    'email_reports',
)

SITE_ID = 1
        
SECRET_KEY = 'secert-key-for-testing'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ROOT_URLCONF = 'email_reports.tests.urls'
