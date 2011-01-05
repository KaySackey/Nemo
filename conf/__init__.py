__author__ = 'Kay Sackey'

import defaults
from django.conf import settings

for setting in dir(defaults):
    if setting == setting.upper() and not hasattr(settings, setting):
        setattr(settings, setting, getattr(defaults, setting))

settings.TEMPLATE_LOADERS = ( 'experiments.nemo.loader', ) + settings.TEMPLATE_LOADERS