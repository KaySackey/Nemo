import os
from django.conf import settings
from experiments.nemo.parser import nemo

MAKO_TEMPLATE_DIRS=(os.path.join(settings.SITE_ROOT, 'templates'),)
MAKO_TEMPLATE_OPTS=dict(input_encoding='utf-8',
                        output_encoding='utf-8',
                        module_directory=os.path.join(settings.SITE_ROOT, 'cache'),
                        preprocessor=nemo
)