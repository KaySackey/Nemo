"""
Mako templates for django >= 1.2.
"""

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.context import Context
from django.template.loaders.filesystem import Loader as FSLoader

from mako.exceptions import MakoException, TopLevelLookupException
from mako.template import Template
from mako.lookup import TemplateLookup


def context_to_dict(ctxt):
    res = {}
    for d in reversed(ctxt.dicts):
        # sometimes contexts will be nested
        if isinstance(d, Context):
            res.update(context_to_dict(d))
        else:
            res.update(d)
    return res


def _get_start_and_end(source, lineno, pos):
    start = 0
    for n, line in enumerate(source.splitlines()):
        if n == lineno:
            start += pos
            break
        else:
            start += len(line) - 1
    return start, start


class MakoExceptionWrapper(Exception):
    def __init__(self, exc, origin):
        self._exc = exc
        self._origin = origin
        self.args = self._exc.args

    def __getattr__(self, name):
        return getattr(self._exc, name)

    @property
    def source(self):
        return (self._origin,
                _get_start_and_end(self._exc.source,
                                   self._exc.lineno,
                                   self._exc.pos))


class MakoTemplate(object):
    def __init__(self, template_obj, origin=None):
        self.template_obj = template_obj
        self.origin = origin

    def render(self, context):
        try:
            return self.template_obj.render_unicode(**context_to_dict(context))
        except MakoException, me:
            if hasattr(me, 'source'):
                raise MakoExceptionWrapper(me, self.origin)
            else:
                raise me

_lookup = None


def get_lookup():
    global _lookup
    if _lookup is None:
        opts = getattr(settings, 'MAKO_TEMPLATE_OPTS', {})
        _lookup = TemplateLookup(directories=settings.MAKO_TEMPLATE_DIRS,
                                 **opts)
    return _lookup


class MakoLoader(FSLoader):
    is_usable = True

    def load_template(self, template_name, template_dirs=None):
        lookup = get_lookup()
        try:
            real_template = lookup.get_template(template_name)
            return MakoTemplate(real_template, template_name), template_name
        except TopLevelLookupException:
            raise TemplateDoesNotExist(
                'mako template not found for name %s' % template_name)
        except MakoException, me:
            if hasattr(me, 'source'):
                raise MakoExceptionWrapper(me, template_name)
            raise me
