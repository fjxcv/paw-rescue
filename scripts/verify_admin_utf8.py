# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHECKS = {
    'frontend/src/constants/site.js': [
        ('\u6696\u722a\u6551\u52a9', 'SITE_NAME'),
        ('\u53ef\u9886\u517b', 'ADOPTION available'),
        ('\u5f85\u5ba1\u6838', 'ONLINE pending'),
    ],
    'frontend/src/pages/AdminDashboard.js': [
        ('\u6570\u636e\u6982\u89c8', 'tab dashboard'),
        ('\u9886\u517b\u5ba1\u6838', 'tab adopt'),
        ('getAuditFormForApp', 'audit fix'),
    ],
    'frontend/src/components/AdminRoute.js': [
        ('\u65e0\u6cd5\u9a8c\u8bc1\u7ba1\u7406\u5458\u6743\u9650', 'auth error'),
    ],
}

MOJIBAKE_SIGNS = ['\u93c6\u67ab\u57d7', '\u9359\u6a59', '\u9422\u5a41']

failed = False
for rel, items in CHECKS.items():
    p = ROOT / rel
    raw = p.read_bytes()
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as e:
        print('FAIL', rel, 'not utf-8:', e)
        failed = True
        continue
    for needle, label in items:
        ok = needle in text
        print(('OK' if ok else 'MISSING'), rel, label)
        if not ok:
            failed = True
    if any(s in text for s in MOJIBAKE_SIGNS):
        print('WARN mojibake chars in', rel)
        failed = True

raise SystemExit(1 if failed else 0)
