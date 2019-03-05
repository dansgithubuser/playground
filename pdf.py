'''
https://resources.infosecinstitute.com/pdf-file-format-basic-structure/
http://lotabout.me/orgwiki/pdf.html
http://wwwimages.adobe.com/www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/PDF32000_2008.pdf
'''

import re
import string
import sys

class Pdf:
    def load(self, file_name):
        with open(file_name, 'rb') as f: content = f.read()
        # split bytes into lines
        lines = ['']
        for i in content:
            if i == ord('\n'): lines.append('')
            else: lines[-1] += chr(i)
        # from the beginning...
        line_i = 0
        # header
        self.header = []
        while lines[line_i].startswith('%'):
            self.header.append(lines[line_i])
            line_i += 1
        # body
        self.objects = {}
        while lines[line_i] not in ['xref', 'startxref']:
            object_number, generation_number, obj = lines[line_i].split()
            if obj != 'obj': raise Exception('expected "obj" on line {} but got "{}"'.format(line_i + 1, obj))
            line_i += 1
            obj = []
            while lines[line_i] != 'endobj':
                obj.append(lines[line_i])
                line_i += 1
            self.objects[(int(object_number), int(generation_number))] = obj
            line_i += 1
        # no idea! adobe prosperity-through-obscurity!
        if lines[line_i] == 'startxref': return self
        # cross-reference table
        line_i += 1
        self.xref = {}
        while lines[line_i] != 'trailer':
            object_0, object_n = [int(i) for i in lines[line_i].split()]
            line_i += 1
            for i in range(object_n):
                split = lines[line_i].split()
                if split[2] not in 'fn': raise Exception('expected "f" or "n" on line {} but got "{}"'.format(line_i + 1, split[2]))
                self.xref[object_0 + i] = {
                    'offset': int(split[0]),
                    'generation': int(split[1]),
                    'free': split[2] == 'f',
                }
                line_i += 1
        # trailer
        line_i += 1
        self.trailer = []
        while lines[line_i] != '%%EOF':
            self.trailer.append(lines[line_i])
            line_i += 1
        # return so we can use soemthing like named constructor idiom
        return self

    def root(self):
        for line in self.trailer:
            m = re.search('/Root ([ 0-9]+) R', line)
            if not m: continue
            object_number, generation_number = [int(i) for i in m.group(1).split()]
            return self.object(object_number, generation_number)

    def object(self, object_number, generation_number=0):
        return self.objects[(object_number, generation_number)]

if __name__ == '__main__':
    pdf = Pdf().load(sys.argv[1])
