__author__ = 'Kay Sackey'

import defaults
from django.conf import settings
from djmako import MakoLoader as loader
from djmako.loader import MakoExceptionWrapper
from shortcuts import *

__all__ = ('render_to_response', 'render_to_string', 'json_response', 'redirect',
           'loader', 'MakoExceptionWrapper', 'defaults')

for setting in dir(defaults):
    if setting == setting.upper() and not hasattr(settings, setting):
        setattr(settings, setting, getattr(defaults, setting))

settings.TEMPLATE_LOADERS = ( 'djmako.MakoLoader', ) + settings.TEMPLATE_LOADERS