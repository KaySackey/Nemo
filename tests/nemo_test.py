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
    result = NemoParser(debug=True).parse(str)
    print result
    return ''
    # return result

    
t = Template(filename=filename,
            preprocessor=nemo,
            input_encoding='utf-8',
            output_encoding='utf-8',)
print t.render()




