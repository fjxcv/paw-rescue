# -*- coding: utf-8 -*-
import os

ROOT = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src')


def fix_file(path):
    with open(path, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    text = None
    used = 'utf-8'
    for enc in ('utf-8', 'gbk', 'gb2312'):
        try:
            t = raw.decode(enc)
            if '\ufffd' not in t:
                text, used = t, enc
                break
        except UnicodeDecodeError:
            continue
    if text is None:
        text = raw.decode('latin1')
        used = 'latin1'
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    return used


def main():
    for dirpath, _, filenames in os.walk(ROOT):
        for name in filenames:
            if name.endswith('.js'):
                p = os.path.join(dirpath, name)
                print(p, fix_file(p))


if __name__ == '__main__':
    main()
