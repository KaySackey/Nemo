import sys
import timeit
from nemo.parser import NemoParser
from mako.template import Template

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print 'A filename is required'
    exit()

def nemo(str, debug=False):
    NemoParser(debug=debug).parse(str)
    # Return Nothing so mako won't render a result
    return ''

def nemo_render(str, debug=False):
    return NemoParser(debug=debug).parse(str)


mako_temp = Template(filename=filename,
            input_encoding='utf-8',
            output_encoding='utf-8',)

nemo_temp = Template(filename=filename,
            preprocessor=nemo,
            input_encoding='utf-8',
            output_encoding='utf-8',)

nemo_temp_render = Template(filename=filename,
            preprocessor=nemo_render,
            input_encoding='utf-8',
            output_encoding='utf-8',)

number = 10000
t_mako = timeit.Timer('mako_temp.render()', 'from __main__ import mako_temp')
t_nemo = timeit.Timer('nemo_temp.render()', 'from __main__ import nemo_temp')
t_nemo_render = timeit.Timer('nemo_temp_render.render()', 'from __main__ import nemo_temp_render')
mako_time = t_mako.timeit(number=number) / number
nemo_time = t_nemo.timeit(number=number) / number
nemo_time_render = t_nemo_render.timeit(number=number) / number

print 'Mako (full render w/o nemo): %.2f ms' % (1000 * mako_time)
print 'Nemo (w/o mako render): %.2f ms' % (1000 * nemo_time)
print 'Nemo (w/ mako render): %.2f ms' % (1000 * nemo_time_render)
