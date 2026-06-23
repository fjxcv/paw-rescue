# -*- coding: utf-8 -*-
"""Fix corrupted Chinese strings in backend Python files."""
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'backend'))

FIXES = {
    'pets/views.py': [
        (
            r'        """[^"]*"""',
            '        """Get pets published by current user via rescue_case."""',
            1,
            72,
        ),
        (
            "'???????????'",
            "'\\u8be5\\u5ba0\\u7269\\u5f53\\u524d\\u4e0d\\u53ef\\u7533\\u8bf7\\u9886\\u517b'",
            1,
        ),
        (
            "'?????????????'",
            "'\\u8be5\\u5ba0\\u7269\\u5df2\\u6709\\u8fdb\\u884c\\u4e2d\\u7684\\u9886\\u517b\\u7533\\u8bf7'",
            1,
        ),
        (
            r"\{'verify_note': '[^']*'\}",
            "{'verify_note': '\\u6838\\u9a8c\\u5931\\u8d25\\u65f6\\u5fc5\\u987b\\u586b\\u5199\\u5931\\u8d25\\u539f\\u56e0'}",
            1,
        ),
    ],
    'pets/serializers.py': [
        (
            "'???????????'",
            "'\\u8be5\\u5ba0\\u7269\\u5f53\\u524d\\u4e0d\\u53ef\\u7533\\u8bf7\\u9886\\u517b'",
            1,
        ),
        (
            "'?????????????'",
            "'\\u8be5\\u5ba0\\u7269\\u5df2\\u6709\\u8fdb\\u884c\\u4e2d\\u7684\\u9886\\u517b\\u7533\\u8bf7'",
            1,
        ),
        (
            "'??????????????'",
            "'\\u60a8\\u5df2\\u63d0\\u4ea4\\u8fc7\\u8be5\\u5ba0\\u7269\\u7684\\u9886\\u517b\\u7533\\u8bf7'",
            1,
        ),
        (
            "'????????????????'",
            "'\\u5df2\\u9886\\u517b\\u5ba0\\u7269\\u4e0d\\u53ef\\u4fee\\u6539\\u516c\\u5f00\\u6216\\u9886\\u517b\\u72b6\\u6001'",
            1,
        ),
        (
            r"\{'audit_opinion': '[^']*'\}",
            "{'audit_opinion': '\\u62d2\\u7edd\\u65f6\\u5fc5\\u987b\\u586b\\u5199\\u9a73\\u56de\\u539f\\u56e0'}",
            1,
        ),
    ],
    'lostfound/serializers.py': [
        (
            "'????? 1 ?????'",
            "'\\u8bf7\\u81f3\\u5c11\\u4e0a\\u4f20 1 \\u5f20\\u5ba0\\u7269\\u7167\\u7247'",
            1,
        ),
    ],
}


def apply_fixes(rel_path, fixes):
    path = os.path.join(ROOT, rel_path)
    text = open(path, 'r', encoding='utf-8', errors='replace').read()
    original = text
    for item in fixes:
        old, new, count = item[0], item[1], item[2]
        if len(item) > 3:
            # line-based docstring fix
            lines = text.splitlines(keepends=True)
            idx = item[3]
            if 0 <= idx < len(lines):
                lines[idx] = re.sub(old, new, lines[idx], count=count)
                text = ''.join(lines)
            continue
        text, n = re.subn(old, new, text, count=count)
        if n == 0 and '?' not in old:
            print('WARN no match', rel_path, old[:40])
    if text != original:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        print('fixed', rel_path)
    else:
        print('unchanged', rel_path)


def main():
    for rel, fixes in FIXES.items():
        apply_fixes(rel, fixes)


if __name__ == '__main__':
    main()
