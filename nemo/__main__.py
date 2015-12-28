"""Nemo - cli

Usage:
    nemo [ - | <src> ] [ <dest> ]

"""
# adapted from: https://raw.githubusercontent.com/tos-kamiya/nemoc/master/src/nemoc.py
import sys
from docopt import docopt, DocoptExit
from nemo.parser import NemoParser
from mako.template import Template


def render(s, params={}):
    r"""
    render(s, params={})

    Returns a rendering result of template s with parameters params.
    The result string is an unicode string.

    >>> render('%img src="images/mrfoobar.jpg" alt="Mr. FooBar"')
    u'\n<img src="images/mrfoobar.jpg" alt="Mr. FooBar" />'
    """

    nemo = NemoParser(debug=False).parse
    return Template(s, preprocessor=nemo).render_unicode(**params)


def main():
    args = docopt(__doc__)
    src = args.get('<src>')
    dest = args.get('<dest>')
    if args.get('-'):
        src_text = sys.stdin.read()
    elif src:
        with open(src, "rb") as f:
            src_text = f.read()
    else:
        raise DocoptExit()
    src_text = src_text.decode('utf-8')
    params = {}

    rendered = render(src_text, params)

    # just a little bit walkaround (this is a mako's spec?)
    rendered = rendered[1:] if rendered.startswith('\n') else rendered
    # same as the above
    rendered = rendered + '\n' if not rendered.endswith('\n') else rendered

    rendered = rendered.encode('utf-8')
    if dest is None:
        sys.stdout.write(rendered)
    else:
        with open(dest, "wb") as f:
            f.write(rendered)

if __name__ == '__main__':
    main()
