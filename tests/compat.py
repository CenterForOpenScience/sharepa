# -*- coding: utf-8 -*-
import sys

PY2 = int(sys.version_info[0]) == 2

if PY2:
    text_type = unicode
else:
    text_type = str
