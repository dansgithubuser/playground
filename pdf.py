'''
https://resources.infosecinstitute.com/pdf-file-format-basic-structure/
http://lotabout.me/orgwiki/pdf.html
http://wwwimages.adobe.com/www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/PDF32000_2008.pdf
'''

import argparse
import re
import os
import pprint
import string
import sys

class Name:
    escape_regex = re.compile('#([0-9a-fA-F]{2})')

    def __init__(self, literal):
        self.value = Name.escape_regex.sub(lambda m: chr(int(m.group(1), 16)), literal)

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return '/{}'.format(self.value)

class Stream:
    def __init__(self, dictionary, stream):
        self.dictionary = dictionary
        self.stream = stream

    def __eq__(self, other):
        return (self.dictionary, self.stream) == (other.dictionary, other.stream)

    def __repr__(self):
        return 'Stream({} {})'.format(pprint.pformat(self.dictionary), hash(self.stream))

class Ref:
    def __init__(self, *args):
        if len(args) == 1:
            literal = args[0]
            self.object_number, self.generation_number = [int(i) for i in literal.split()[:2]]
        elif len(args) == 2:
            self.object_number, self.generation_number = args
        else:
            raise Exception('wrong number of arguments')

    def __eq__(self, other):
        return (self.object_number, self.generation_number) == (other.object_number, other.generation_number)

    def __hash__(self):
        return hash((self.object_number, self.generation_number))

    def __repr__(self):
        return '{} {}'.format(self.object_number, self.generation_number)

class Parser:
    def __init__(self, content):
        self.line = 1
        self.content = content
        self.i = 0

    def _advance(self, i, _depth=0):
        advanced = self.content[self.i:i]
        self.line += advanced.count(b'\n')
        self.i = i
        if os.environ.get('DEBUG'): print('{}advanced to {}: {}'.format('\t' * _depth, self.i, advanced))

    def check(self, pattern):
        m = re.match(pattern.encode(), self.content[self.i:])
        return m

    def parse(self, pattern, allow_nonmatch=False, skip_space=True, binary=False, _depth=0):
        m = self.check(pattern)
        if not m or not len(m.group()):
            if allow_nonmatch: return
            raise Exception("parse failed on line {}, index {}; expected {}, got {}".format(
                self.line, self.i, repr(pattern), repr(self.check('(.*?)(\n|\r|$)').group(1))
            ))
        self._advance(self.i + len(m.group()), _depth=_depth)
        if skip_space: self.parse('\s*', allow_nonmatch=True, skip_space=False, _depth=_depth)
        if binary:
            decode = lambda x: x
        else:
            decode = lambda x: x.decode()
        if m.groups():
            result = [decode(i) for i in m.groups()]
        else:
            result = decode(m.group())
        return result

    def parse_object(self, _depth=0):
        def transform_number(x):
            try: return int(x)
            except Exception: pass
            return float(x)
        not_raw_paren = (
            r'(?:'
                r'[^()]|\\\(|\\\)'
            r')*'
        )
        pattern_string_literal = (
            r'\(('
                + not_raw_paren +
                r'(?:'  # allow balanced raw parens
                    r'\('
                    + not_raw_paren +
                    '\)'
                r')*'
                + not_raw_paren +
            r')\)'
        )
        def transform_string_literal(x):
            for k, v in {
                r'\n': '\n',
                r'\r': '\r',
                r'\t': '\t',
                r'\b': '\b',
                r'\f': '\f',
                r'\(': '(',
                r'\)': ')',
                r'\\': '\\',
            }.items(): x = x.replace(k, v)
            r = re.compile(r'\\([0-8]{1,3})')
            x = r.sub(lambda m: chr(int(m.group(1), 8)), x)
            return x
        def transform_string_hexadecimal(x):
            result = ''
            for i in range(0, len(x), 2):
                o = int(x[i], 16) * 16
                if i + 1 < len(x): o += int(x[i + 1], 16)
                result += chr(o)
            return result
        name_sentinel = '(?=' + '|'.join([
            r'\s',
            # according to ISO, seems name end should be indicated by space, but in practice we see other shenanigans
            '/',
            r'\(',
            r'\[', r'\]',
            '<', '>',
        ]) + ')'
        pattern_name = '/(.*?)' + name_sentinel
        def transform_array(x):
            result = []
            while not self.parse(']', allow_nonmatch=True, _depth=_depth):
                result.append(self.parse_object(_depth=_depth + 1))
            return result
        def transform_dictionary_or_stream(x):
            result = {}
            while not self.parse('>>', allow_nonmatch=True, _depth=_depth):
                entry = Name(self.parse(pattern_name, _depth=_depth)[0])
                result[entry.value] = self.parse_object(_depth=_depth + 1)
            if self.parse('stream', allow_nonmatch=True, skip_space=False, _depth=_depth):
                l = result['Length']
                e = self.content.find(b'endstream', self.i + l) - 1
                result = Stream(result, self.content[e - l:e])
                self._advance(e)
                self.parse(r'\s*endstream', _depth=_depth)
            return result
        for pattern, transform in [
            (pattern_name, lambda x: Name(x[0])),
            ('\d+ \d+ R', Ref),
            (r'[+-]?\d?\.?\d*', transform_number),
            (pattern_string_literal, lambda x: transform_string_literal(x[0])),
            (r'<<', transform_dictionary_or_stream),
            (r'\[', transform_array),
            ('<(.*?)>', lambda x: transform_string_hexadecimal(x[0])),
            ('true', lambda x: True),
            ('false', lambda x: False),
        ]:
            obj = self.parse(pattern, allow_nonmatch=True, _depth=_depth)
            if obj is not None: return transform(obj)
        raise Exception('unknown object at line {}, index {}'.format(self.line, self.i))

class Pdf:
    def __repr__(self):
        return (
            '===== header =====\n'
            '{}\n'
            '\n'
            '===== objects =====\n'
            '{}\n'
            '\n'
            '===== xref =====\n'
            '{}\n'
            '\n'
            '===== trailer =====\n'
            '{}'
        ).format(self.header, pprint.pformat(self.objects), pprint.pformat(self.xref), pprint.pformat(self.trailer))

    def __getitem__(self, key):
        if type(key) == int: return self.object(key)
        elif isinstance(key, Ref): return self.objects[key]
        else: raise Exception('bad key type')

    def load(self, file_name):
        with open(file_name, 'rb') as f: parser = Parser(f.read())
        # header
        self.header = [parser.parse(r'%([^\n\r]*)')]
        x = parser.parse(r'%([^\n\r]*)', allow_nonmatch=True, binary=True)
        if x: self.header.append(x[0])
        # body
        self.objects = {}
        while not parser.check('xref|startxref'):
            ref = Ref(parser.parse(r'\d+ \d+ obj'))
            self.objects[ref] = parser.parse_object()
            parser.parse('endobj')
        # XFA
        if parser.check('startxref'):
            raise Exception("sorry, this isn't actually a PDF, it looks to be XFA")
        # cross-reference table
        parser.parse('xref')
        self.xref = {}
        while not parser.check('trailer'):
            object_0, object_n = [int(i) for i in parser.parse(r'[^\n\r]*').split()]
            for i in range(object_n):
                ref, free = parser.parse('(\d+ \d+) ([fn])')
                self.xref[object_0 + i] = {
                    'ref': Ref(ref),
                    'free': free == 'f',
                }
        # trailer
        parser.parse('trailer')
        dictionary = parser.parse_object()
        parser.parse('startxref')
        startxref = int(parser.parse('\d+'))
        self.trailer = {
            'dictionary': dictionary,
            'startxref': startxref,
        }
        parser.parse('%%EOF')
        assert(parser.i == len(parser.content))
        # return so we can use something like named constructor idiom
        return self

    def root(self):
        return self.objects[self.trailer['dictionary']['Root']]

    def object(self, object_number, generation_number=0):
        return self.objects[Ref(object_number, generation_number)]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pdf')
    parser.add_argument('--compare', '-c')
    args = parser.parse_args()
    pdf = Pdf().load(args.pdf)
    if args.compare:
        other = Pdf().load(args.compare)
        for k, v in pdf.objects.items():
            if k not in other.objects:
                print('===== {} ===== missing from other'.format(k))
            if other.objects[k] != v:
                print((
                    '===== {} =====\n'
                    '{}\n'
                    '\n'
                    '===== other =====\n'
                    '{}'
                ).format(k, v, other.objects[k]))
        for k in other.objects.keys():
            if k not in pdf.objects:
                print('===== {} ===== missing'.format(k))
