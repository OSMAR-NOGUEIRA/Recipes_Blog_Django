import os

from .installed_apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE

    
ACCOUNT_ADAPTER = 'authors.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'authors.adapters.SocialAccountAdapter'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS += [    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    #Providers
    'allauth.socialaccount.providers.apple',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    ]

MIDDLEWARE += ["allauth.account.middleware.AccountMiddleware",]

SOCIALACCOUNT_PROVIDERS = {
  'google': {
      'EMAIL_AUTHENTICATION': True
  }
}

SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

LOGIN_REDIRECT_URL = '/'

ACCOUNT_AUTHENTICATION_METHOD = 'email'

ACCOUNT_EMAIL_REQUIRED = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID', None),
            'secret': os.environ.get('GOOGLE_SECRET', None),
            'key': ''
        }
    }
}
