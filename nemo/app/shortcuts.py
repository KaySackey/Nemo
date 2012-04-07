"""
 Defines variations on render_to_string and render_to_response that will optionally only render a single mako def
"""

from mako.exceptions import MakoException
from django.template.loader import get_template, select_template
from djmako.loader import context_to_dict
from django.template.context import Context, RequestContext
from django.http import HttpResponse
from django.utils import simplejson
from djmako.loader import MakoExceptionWrapper

from django.shortcuts import redirect

__all__ = ('redirect', 'render_to_string', 'render_to_response', 'json_response', 'render')

## Patched from on MakoTemplate.render()
def render_nemo_template(mako_template, context, def_name):
    try:
        template_obj = mako_template.template_obj

        if def_name is not None:
            template_obj = mako_template.template_obj.get_def(def_name)

        return template_obj.render_unicode(**context_to_dict(context))
    except MakoException, me:
        if hasattr(me, 'source'):
            raise MakoExceptionWrapper(me, mako_template.origin)
        else:
            raise me


def render_to_string(template_name, dictionary=None, context_instance=None, def_name=None):
    """
    Loads the given template_name and renders it with the given dictionary as
    context. The template_name may be a string to load a single template using
    get_template, or it may be a tuple to use select_template to find one of
    the templates in the list. Returns a string.
    """
    dictionary = dictionary or {}
    if isinstance(template_name, (list, tuple)):
        t = select_template(template_name)
    else:
        t = get_template(template_name)
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = Context(dictionary)

    return render_nemo_template(t, context_instance, def_name)


def render_to_response(*args, **kwargs):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None),
                           'status': kwargs.pop('status', None),
                           'content_type': kwargs.pop('content_type', None)
                           }
    return HttpResponse(render_to_string(*args, **kwargs), **httpresponse_kwargs)

def json_response(obj, **kwargs):
    return HttpResponse(simplejson.dumps(obj), **kwargs)

def render(request, *args, **kwargs):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    Uses a RequestContext by default.
    """
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None),
                           'status': kwargs.pop('status', None),
                           'content_type': kwargs.pop('content_type', None)
                           }

    if 'context_instance' in kwargs:
        context_instance = kwargs.pop('context_instance')
        if kwargs.get('current_app', None):
            raise ValueError('If you provide a context_instance you must '
                             'set its current_app before calling render()')
    else:
        current_app = kwargs.pop('current_app', None)
        context_instance = RequestContext(request, current_app=current_app)

    kwargs['context_instance'] = context_instance

    return HttpResponse(render_to_string(*args, **kwargs), **httpresponse_kwargs)