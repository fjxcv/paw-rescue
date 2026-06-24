# -*- coding: utf-8 -*-
"""Second pass: fix remaining Home.js / LostFoundList.js mojibake."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sub1(pattern, fn, text, count=1):
    return re.sub(pattern, lambda m: fn(m), text, count=count)


def fix_home(path: Path) -> None:
    t = path.read_text(encoding='utf-8')

    t = sub1(
        r'\{/\* [^*]+ \*/\}(\s*\n\s*\{!carouselLoading)',
        lambda m: '{/* \u8f6e\u64ad\u56fe */}' + m.group(1),
        t,
    )
    t = sub1(
        r'(<button className="carousel-control-next"[^>]*>\s*<span className="carousel-control-next-icon"[^/]*/>\s*)<span className="visually-hidden">[^<]*</span>',
        lambda m: m.group(1) + '<span className="visually-hidden">\u4e0b\u4e00\u5f20</span>',
        t,
    )
    t = sub1(
        r'(<span className="badge bg-warning text-dark ms-1">)[^<]+(\{item\.reward_amount\})',
        lambda m: m.group(1) + '\u60a9\u8d4f \u00a5' + m.group(2),
        t,
    )
    t = sub1(
        r'(<p className="text-muted small mb-0">)[^<]+(</p>\s*\n\s*<Link to="/lost-found")',
        lambda m: m.group(1) + '\u6682\u65e0\u62a5\u5931\u4fe1\u606f' + m.group(2),
        t,
    )
    t = sub1(
        r'(<p className="text-muted small mb-0">)[^<]+(</p>\s*\n\s*<Link to="/cms\?type=science")',
        lambda m: m.group(1) + '\u6682\u65e0\u79d1\u666e\u6587\u7ae0' + m.group(2),
        t,
    )
    t = sub1(
        r'(<p className="text-muted small mb-0">)[^<]+(</p>\s*\n\s*<Link to="/cms\?type=announcement")',
        lambda m: m.group(1) + '\u6682\u65e0\u516c\u544a' + m.group(2),
        t,
    )
    t = sub1(
        r'(<Link to="/pets"[^>]*>\s*<i className="fas fa-search me-2 btn-icon"></i>\s*)[^\n<]+',
        lambda m: m.group(1) + '\u6d4f\u89c8\u5ba0\u7269',
        t,
    )
    t = sub1(
        r'(<Link to="/register"[^>]*>\s*<i className="fas fa-users me-2 btn-icon"></i>\s*)[^\n<]+',
        lambda m: m.group(1) + '\u52a0\u5165\u793e\u533a',
        t,
    )
    t = sub1(
        r"alert\('[^']*'\)(\s*\n\s*\}\s*\}\s*/>)",
        lambda m: "alert('\u4e0a\u4f20\u5931\u8d25')" + m.group(1),
        t,
    )

    path.write_text(t, encoding='utf-8', newline='\n')


def fix_lf(path: Path) -> None:
    t = path.read_text(encoding='utf-8')
    t = t.replace('// \u60a9\u8d4f\u7b5b\n', '// \u60a9\u8d4f\u7b5b\u9009\n')
    path.write_text(t, encoding='utf-8', newline='\n')


if __name__ == '__main__':
    fix_home(ROOT / 'frontend/src/pages/Home.js')
    fix_lf(ROOT / 'frontend/src/pages/LostFoundList.js')
    print('pass2 done')
