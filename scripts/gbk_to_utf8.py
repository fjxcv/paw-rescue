# -*- coding: utf-8 -*-
"""Deprecated: use ensure_utf8.py instead."""
import subprocess
import sys
import os

if __name__ == '__main__':
    script = os.path.join(os.path.dirname(__file__), 'ensure_utf8.py')
    sys.exit(subprocess.call([sys.executable, script] + sys.argv[1:]))
