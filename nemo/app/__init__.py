"""
Provides integration with Django
"""

__author__ = 'Kay Sackey'

import defaults
from django.conf import settings
from djmako import MakoLoader as loader
from djmako.loader import MakoExceptionWrapper
from shortcuts import *

import inspect
import logging
import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
try:
    from django.utils import importlib
except ImportError:
    import importlib

__all__ = ('render_to_response', 'render_to_string', 'json_response', 'redirect',
           'loader', 'MakoExceptionWrapper', 'defaults', 'render')

# Collect Settings from Django Conf
for setting in dir(defaults):
    if setting == setting.upper() and not hasattr(settings, setting):
        setattr(settings, setting, getattr(defaults, setting))

# Add Mako to template loaders
settings.TEMPLATE_LOADERS = ( 'nemo.app.loader.MakoLoader', ) + settings.TEMPLATE_LOADERS

# Connect Nemo up with Mako
if 'preprocessor' not in settings.MAKO_TEMPLATE_OPTS:
    from nemo.parser import nemo
    settings.MAKO_TEMPLATE_OPTS['preprocessor'] = nemo

# Auto Discover
############

# Setup default logging.
log = logging.getLogger('nemo')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)

def autodiscover():
    """
    Automatically build the template directory list.
    Almost exactly as django.contrib.admin does things, for consistency.
    """
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        # For each app, we look for a mako_templates directory with a file '.__mako__' within it
        # If it exists we add it to the MAKO_TEMPLATE_DIRS
        try:
            app_path = importlib.import_module(app).__path__
        except AttributeError:
            continue

        template_directory = os.path.join(app_path[0], 'templates')
        special_file = os.path.join(template_directory, '.__mako__')

        settings.MAKO_TEMPLATE_DIRS = list(settings.MAKO_TEMPLATE_DIRS)

        if os.path.exists( special_file ):
            settings.MAKO_TEMPLATE_DIRS.append(template_directory)