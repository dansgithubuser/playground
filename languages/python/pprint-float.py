#!/usr/bin/env python3

import pprint

class PrettierPrinter(pprint.PrettyPrinter):
    def __init__(self, formats, **kwargs):
        pprint.PrettyPrinter.__init__(self, **kwargs)
        self.formats = formats

    def format(self, object, context, maxlevels, level):
        fmt = self.formats.get(type(object))
        if fmt == None:
            pass
        elif callable(fmt):
            return (
                fmt(
                    object,
                    lambda object: self.format(object, context, maxlevels, level + 1)[0],
                ),
                True,
                False,
            )
        elif type(fmt) == str:
            return self.formats[type(object)].format(object), True, False
        else:
            raise Exception('Unknown format: {fmt}')
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

def fmt_float(x, _fmt):
    if 1e-2 < x < 100:
        return f' {x:.3f}'
    if -100 < x < -1e-2:
        return f'{x:.3f}'
    return f'{x:.3e}'

def ppprint(
    x,
    formats={
        float: fmt_float,
        list: lambda x, fmt: ' '.join([fmt(i) for i in x]),
    },
    width=80,
    compact=True,
):
    PrettierPrinter(formats, width=width, compact=compact).pprint(x)

x = [1/3, 2/3, 3/3]
pprint.pprint(x)
ppprint(x, {float: '{:.2}'})
