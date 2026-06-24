# -*- coding: utf-8 -*-
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src')


def main():
    bad = []
    for dirpath, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith('.js'):
                continue
            path = os.path.join(dirpath, fn)
            try:
                text = open(path, encoding='utf-8').read()
            except UnicodeDecodeError:
                bad.append((path, 0, 'UTF-8 decode error'))
                continue
            for i, line in enumerate(text.splitlines(), 1):
                if '??' not in line:
                    continue
                if 'http' in line or 'placeholder' in line:
                    continue
                if '??' in line and 'dashboard' in line.lower():
                    continue
                if re.search(r"['\"][^'\"]*\?\?+[^'\"]*['\"]", line):
                    bad.append((path, i, line.strip()[:100]))
    print('issues:', len(bad))
    for item in bad:
        print(item)


if __name__ == '__main__':
    main()
