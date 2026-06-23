# -*- coding: utf-8 -*-
"""Direct fixes for remaining Home.js mojibake."""
import re
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'frontend/src/pages/Home.js'
t = path.read_text(encoding='utf-8')


def sub(pattern, fn, s, count=0):
    return re.sub(pattern, lambda m: fn(m), s, count=count)


t = sub(
    r'\{/\* [^*]+ \*/\}(\s*\n\s*\{!carouselLoading)',
    lambda m: '{/* \u8f6e\u64ad\u56fe */}' + m.group(1),
    t,
    1,
)
t = sub(r'>\u6d58\u5b09[\u7acb\u5bc7\ufffd]+</span>', lambda _m: '>\u4e0b\u4e00\u5f20</span>', t, 1)
t = sub(r'>\u60a9\u8d4f \u00a5', lambda _m: '>\u60ac\u8d4f \u00a5', t, 0)
t = sub(
    r'<p className="text-muted small mb-0">[^<]+</p>\s*\n\s*\)\}\s*\n\s*<Link to="/lost-found"',
    lambda _m: '<p className="text-muted small mb-0">\u6682\u65e0\u62a5\u5931\u4fe1\u606f</p>\n                  )}\n                  <Link to="/lost-found"',
    t,
    1,
)
t = sub(
    r'<p className="text-muted small mb-0">[^<]+</p>\s*\n\s*\)\}\s*\n\s*<Link to="/cms\?type=science"',
    lambda _m: '<p className="text-muted small mb-0">\u6682\u65e0\u79d1\u666e\u6587\u7ae0</p>\n                  )}\n                  <Link to="/cms?type=science"',
    t,
    1,
)
t = sub(
    r'<p className="text-muted small mb-0">[^<]+</p>\s*\n\s*\)\}\s*\n\s*<Link to="/cms\?type=announcement"',
    lambda _m: '<p className="text-muted small mb-0">\u6682\u65e0\u516c\u544a</p>\n                  )}\n                  <Link to="/cms?type=announcement"',
    t,
    1,
)
t = sub(r"alert\('\u6d58\u59d0[^']*'\)", lambda _m: "alert('\u4e0a\u4f20\u5931\u8d25')", t, 1)
t = sub(r'\{/\* \u7039[^*]+\*/\}', lambda _m: '{/* \u5ba0\u7269\u5206\u7c7b */}', t, 1)

path.write_text(t, encoding='utf-8', newline='\n')
print('direct fix done')
