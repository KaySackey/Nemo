import sys
from nemo.parser import NemoParser
from mako.template import Template

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print 'A filename is required'
    exit()

def nemo(str, debug=False):
    if debug: print "[Debug]---------  %s --------------[Debug]\n" % filename

    result = NemoParser(debug=debug).parse(str)

    if debug: print "\n[Debug]---------  Result --------------[Debug]"
    print result

    # Return Nothing so mako won't render a result
    return ''


t = Template(filename=filename,
            preprocessor=nemo,
            input_encoding='utf-8',
            output_encoding='utf-8',)
print t.render()




