#!/usr/bin/env python3

import pprint

class PrettierPrinter(pprint.PrettyPrinter):
    def __init__(self, formats):
        pprint.PrettyPrinter.__init__(self)
        self.formats = formats

    def format(self, object, context, maxlevels, level):
        if type(object) in self.formats:
            return self.formats[type(object)].format(object), 1, 0
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

def ppprint(x, formats={}):
    PrettierPrinter(formats).pprint(x)

x = [1/3, 2/3, 3/3]
pprint.pprint(x)
ppprint(x, {float: '{:.2}'})
