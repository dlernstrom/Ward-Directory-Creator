# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os


path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.git',
                    'refs', 'heads', 'master')
try:
    with open(path, 'r') as f:
        __version__ = f.read().strip()[:7]
except IOError:
    __version__ = 'testing'
