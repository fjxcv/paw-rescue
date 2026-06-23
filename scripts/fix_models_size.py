# -*- coding: utf-8 -*-
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'backend' / 'pets' / 'models.py'
lines = path.read_bytes().splitlines(keepends=True)
out = []
for i, line in enumerate(lines):
    if b"('small'," in line and i < 20:
        out.append(b"        ('small', '\\u5c0f\\u578b'),\n")
    elif b"('medium'," in line and i < 20:
        out.append(b"        ('medium', '\\u4e2d\\u578b'),\n")
    elif b"('large'," in line and i < 20:
        out.append(b"        ('large', '\\u5927\\u578b'),\n")
    else:
        out.append(line)
path.write_bytes(b''.join(out))
print('fixed', path)
