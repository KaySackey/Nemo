import sys
from parser import NemoParser
from mako.template import Template

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print 'A filename is required'
    exit()

def nemo(str):
    print "---------  %s --------------" % filename
    # Return a result to Mako which will then render the string
    return NemoParser(debug=False).parse(str)

t = Template(filename=filename,
            preprocessor=nemo,
            input_encoding='utf-8',
            output_encoding='utf-8',)
print t.render()