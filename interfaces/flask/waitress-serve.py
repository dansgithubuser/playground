#!/usr/bin/env python3

import hello

from waitress import serve

serve(hello.app, listen='*:5000')
