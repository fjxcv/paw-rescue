# -*- coding: utf-8 -*-
"""Fix mojibake in frontend pages - ASCII source, unicode escapes only."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sub1(pattern, repl_fn, text, count=1):
    return re.sub(pattern, lambda m: repl_fn(m), text, count=count)


def fix_home(path: Path) -> None:
    t = path.read_text(encoding='utf-8', errors='replace')

    t = sub1(
        r'\{/\* [^*]+ \*/\}(\s*\n\s*!\{!carouselLoading)',
        lambda m: '{/* \u8f6e\u64ad\u56fe */}' + m.group(1),
        t,
    )
    t = sub1(
        r'\{/\* [^*]+ \*/\}(\s*\n\s*<div className="container py-4">\s*\n\s*<h4[^>]*>\s*\n\s*<i className="fas fa-chart-bar)',
        lambda m: '{/* \u6838\u5fc3\u6570\u636e\u7edf\u8ba1 */}' + m.group(1),
        t,
    )
    t = sub1(
        r'\{/\* [^*]+ \*/\}(\s*\n\s*<div className="container py-4">\s*\n\s*<h4[^>]*>\s*\n\s*<i className="fas fa-bolt)',
        lambda m: '{/* \u6700\u65b0\u805a\u5408\u52a8\u6001 */}' + m.group(1),
        t,
    )
    t = sub1(r'\{/\* Hero [^*]+ \*/\}', lambda _m: '{/* Hero \u533a\u57df */}', t)
    t = sub1(r'\{/\* AI [^*]+ \*/\}', lambda _m: '{/* AI \u54c1\u79cd\u8bc6\u522b */}', t)
    t = sub1(
        r'\{/\* [^*]+ \*/\}(\s*\n\s*<div className="pet-categories-section")',
        lambda m: '{/* \u5ba0\u7269\u5206\u7c7b */}' + m.group(1),
        t,
    )
    t = sub1(
        r'(<button className="carousel-control-next"[^>]*>\s*<span className="carousel-control-next-icon"[^/]*/>\s*)<span className="visually-hidden">[^<]*</span>',
        lambda m: m.group(1) + '<span className="visually-hidden">\u4e0b\u4e00\u5f20</span>',
        t,
    )
    t = sub1(
        r'(<span className="badge bg-warning text-dark ms-1">)[^<]*(\{item\.reward_amount\})',
        lambda m: m.group(1) + '\u60a9\u8d4f \u00a5' + m.group(2),
        t,
    )
    t = sub1(
        r'(<p className="text-muted small mb-0">)[^<]+(</p>\s*\n\s*<Link to="/lost-found")',
        lambda m: m.group(1) + '\u6682\u65e0\u62a5\u5931\u4fe1\u606f' + m.group(2),
        t,
    )
    t = sub1(
        r'(<i className="fas fa-graduation-cap me-2"></i>)[^\n<]+',
        lambda m: m.group(1) + '\u79d1\u666e\u6587\u7ae0',
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
        r'(<span className="text-dark">)[^<]+(</span>\s*\n\s*<br)',
        lambda m: m.group(1) + '\u5bfb\u627e\u4f60\u7684' + m.group(2),
        t,
    )
    t = sub1(
        r'(<span className="text-warning">)[^<]+(</span>\s*\n\s*</h1>)',
        lambda m: m.group(1) + '\u5b8c\u7f8e\u5ba0\u7269\u4f19\u4f34' + m.group(2),
        t,
    )
    t = sub1(
        r'(\{SITE_NAME\} )[^\n]+(\s*</p>\s*\n\s*<div className="d-flex justify-content-center gap-3)',
        lambda m: m.group(1) + '\u8fde\u63a5\u7231\u5fc3\u4eba\u58eb\u4e0e\u5f85\u9886\u517b\u5ba0\u7269\uff0c\u53c2\u4e0e\u6d41\u6d6a\u52a8\u7269\u6551\u52a9\uff0c\u5171\u5efa\u6e29\u6696\u7684\u4eba\u5ba0\u793e\u533a\u3002' + m.group(2),
        t,
    )
    t = sub1(
        r'(<i className="fas fa-search me-2 btn-icon"></i>\s*)[^\n<]+(</Link>)',
        lambda m: m.group(1) + '\u6d4f\u89c8\u5ba0\u7269' + m.group(2),
        t,
    )
    t = sub1(
        r'(<i className="fas fa-users me-2 btn-icon"></i>\s*)[^\n<]+(</Link>)',
        lambda m: m.group(1) + '\u52a0\u5165\u793e\u533a' + m.group(2),
        t,
    )
    t = sub1(
        r'(<p className="text-muted small">)[^<]+(</p>\s*\n\s*<div className="row g-2 align-items-end">)',
        lambda m: m.group(1) + '\u4e0a\u4f20\u5ba0\u7269\u7167\u7247\u540e\uff0c\u5c06\u4f7f\u7528\u57fa\u4e8e Oxford-IIIT Pet \u7b49\u516c\u5f00\u6570\u636e\u96c6\u8bad\u7ec3\u7684\u672c\u5730 CNN \u6a21\u578b\u8bc6\u522b\u54c1\u79cd\uff08Top \u5019\u9009\u4e0e\u7f6e\u4fe1\u5ea6\uff09\u3002' + m.group(2),
        t,
    )
    t = sub1(
        r'(<label className="form-label small">)[^<]+(</label>\s*\n\s*<input type="file")',
        lambda m: m.group(1) + '\u4e0a\u4f20\u56fe\u7247' + m.group(2),
        t,
    )
    t = sub1(
        r"alert\('[^']*'\)(\s*\n\s*\}\s*\}\s*/>)",
        lambda m: "alert('\u4e0a\u4f20\u5931\u8d25')" + m.group(1),
        t,
    )
    t = sub1(
        r'(<label className="form-label small">)[^<]+(</label>\s*\n\s*<input className="form-control form-control-sm" value=\{aiDesc\})',
        lambda m: m.group(1) + '\u6587\u5b57\u63cf\u8ff0\uff08\u53ef\u9009\uff09' + m.group(2),
        t,
    )
    t = sub1(
        r"if \(!localStorage\.getItem\('token'\)\) \{ alert\('[^']*'\)",
        lambda _m: "if (!localStorage.getItem('token')) { alert('\u8bf7\u5148\u767b\u5f55')",
        t,
    )
    t = sub1(
        r"if \(!aiImageUrl\) \{ alert\('[^']*'\)",
        lambda _m: "if (!aiImageUrl) { alert('\u8bf7\u5148\u4e0a\u4f20\u56fe\u7247')",
        t,
    )
    t = sub1(
        r"msg = '[^']*10[^']*30[^']*'",
        lambda _m: "msg = '\u8bc6\u522b\u8d85\u65f6\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5\uff08AI \u5206\u6790\u7ea6\u9700 10\u201330 \u79d2\uff09'",
        t,
    )
    t = sub1(
        r"msg = err\.message \|\| '[^']*'",
        lambda _m: "msg = err.message || '\u8bc6\u522b\u5931\u8d25\uff0c\u8bf7\u786e\u8ba4\u5df2\u767b\u5f55\u4e14\u540e\u7aef\u5df2\u542f\u52a8'",
        t,
    )

    # section comments for dashboard columns
    t = t.replace(
        '            {/* \u7d27\u6025\u5bfb\u4e3b */}\n            <div className="col-md-4">\n              <div className="card shadow-sm h-100">\n                <div className="card-header bg-success text-white">',
        '            {/* \u79d1\u666e\u6587\u7ae0 */}\n            <div className="col-md-4">\n              <div className="card shadow-sm h-100">\n                <div className="card-header bg-success text-white">',
        1,
    )
    t = t.replace(
        '            {/* \u7d27\u6025\u5bfb\u4e3b */}\n            <div className="col-md-4">\n              <div className="card shadow-sm h-100">\n                <div className="card-header bg-warning text-dark">',
        '            {/* \u6700\u65b0\u516c\u544a */}\n            <div className="col-md-4">\n              <div className="card shadow-sm h-100">\n                <div className="card-header bg-warning text-dark">',
        1,
    )

    path.write_text(t, encoding='utf-8', newline='\n')


def fix_lostfound(path: Path) -> None:
    t = path.read_text(encoding='utf-8', errors='replace')
    t = re.sub(r'[\ufffd\uFFFD]{0,2}1[\ufffd\uFFFD]7', '', t)
    t = re.sub(r'[\ufffd\uFFFD]+', '', t)

    t = sub1(r"label: '\u5168\u90e8\u72b6[^']*'", lambda _m: "label: '\u5168\u90e8\u72b6\u6001'", t)
    t = sub1(r'// \u56fa\u5b9a\u7528\u6237\u4f4d\u7f6e\uff0c\u907f\u514d\u91cd\u590d\u5b9a[^\n]*', lambda _m: '// \u56fa\u5b9a\u7528\u6237\u4f4d\u7f6e\uff0c\u907f\u514d\u91cd\u590d\u5b9a\u4f4d', t)
    t = sub1(r'// \u60a9\u8d4f\u7b5b[^\n]*', lambda _m: '// \u60a9\u8d4f\u7b5b\u9009', t)
    t = sub1(r"setError\('\u52a0\u8f7d\u4fe1\u606f\u5931\u8d25[^\']*'\)", lambda _m: "setError('\u52a0\u8f7d\u4fe1\u606f\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5\u3002')", t)
    t = sub1(r'// \u9644\u8fd1\u6a21\u5f0f\u4e0b\uff0c\u7b5b[^\n]*', lambda _m: '// \u9644\u8fd1\u6a21\u5f0f\u4e0b\uff0c\u7b5b\u9009\u6761\u4ef6\u53d8\u5316\u65f6\u81ea\u52a8\u91cd\u65b0\u641c\u7d22', t)
    t = sub1(r'// doNearbySearch \u4f1a\u7531\u4e0a\u9762\u7684[^\n]*useEffect[^\n]*', lambda _m: '// doNearbySearch \u4f1a\u7531\u4e0a\u9762\u7684 useEffect \u81ea\u52a8\u89e6\u53d1', t)
    t = sub1(r"msg = '\u4f4d\u7f6e\u4fe1\u606f\u4e0d\u53ef[^\']*'", lambda _m: "msg = '\u4f4d\u7f6e\u4fe1\u606f\u4e0d\u53ef\u7528'", t)
    t = sub1(r'// \u9000\u51fa\u9644\u8fd1\u641c\u7d22\u6a21[^\n]*', lambda _m: '// \u9000\u51fa\u9644\u8fd1\u641c\u7d22\u6a21\u5f0f', t)
    t = sub1(r'// \u4f7f\u7528 Leaflet \u6784\u5efa\u5e26\u591a\u4e2a\u6807\u8bb0\u70b9\u7684\u5730[^\n]*HTML', lambda _m: '// \u4f7f\u7528 Leaflet \u6784\u5efa\u5e26\u591a\u4e2a\u6807\u8bb0\u70b9\u7684\u5730\u56fe HTML', t)
    t = sub1(r'// \u6784\u5efa\u6807\u8bb0[^\n]*JS \u4ee3\u7801', lambda _m: '// \u6784\u5efa\u6807\u8bb0\u70b9 JS \u4ee3\u7801', t)
    t = sub1(r'// \u7528\u6237\u4f4d\u7f6e\uff08\u817e\u8baf\u5730\u56fe\u98ce\u683c\u5b9a\u4f4d\u56fe[^\n]*', lambda _m: '// \u7528\u6237\u4f4d\u7f6e\uff08\u817e\u8baf\u5730\u56fe\u98ce\u683c\u5b9a\u4f4d\u56fe\u6807 - \u84dd\u8272\u6c34\u6ef4\u5f62\uff09', t)
    t = sub1(r'\{/\* \u9644\u8fd1\u641c\u7d22\u63a7\u5236[^\n]*\*/\}', lambda _m: '{/* \u9644\u8fd1\u641c\u7d22\u63a7\u5236\u680f */}', t)
    t = sub1(r'\u641c\u7d22\u8303\u56f4[^\n<]*</label>', lambda _m: '\u641c\u7d22\u8303\u56f4\uff1a</label>', t)
    t = sub1(r'\{/\* \u641c\u7d22\u548c\u7b5b[^\n]*\*/\}', lambda _m: '{/* \u641c\u7d22\u548c\u7b5b\u9009 */}', t)
    t = sub1(r'placeholder="[^"]*"', lambda _m: 'placeholder="\u641c\u7d22\u7269\u79cd\u3001\u7279\u5f81\u3001\u5730\u5740..."', t)
    t = sub1(r'>\u4ec5\u770b\u6709\u60a9[^\n<]*</label>', lambda _m: '>\u4ec5\u770b\u6709\u60a9\u8d4f</label>', t)
    t = sub1(r'>\u52a0\u8f7d[^\n<]*\.\.\.</span>', lambda _m: '>\u52a0\u8f7d\u4e2d...</span>', t)
    t = sub1(r'>\u60a9\u8d4f \{post\.reward_amount\} [^\n<]*</p>', lambda _m: '>\u60a9\u8d4f {post.reward_amount} \u5143</p>', t)
    t = sub1(r'title="\u6807\u8bb0\u5df2\u627e[^\"]*"', lambda _m: 'title="\u6807\u8bb0\u5df2\u627e\u5230"', t)
    t = sub1(r"confirm\('\u786e\u5b9a\u8981\u64a4[^\']*'\)", lambda _m: "confirm('\u786e\u5b9a\u8981\u64a4\u9500\u8fd9\u6761\u53d1\u5e03\u5417\uff1f')", t)

    path.write_text(t, encoding='utf-8', newline='\n')


def fix_utf8_rule(path: Path) -> None:
    text = (
        '---\n'
        'description: Prevent Chinese mojibake - all source must be UTF-8 on disk\n'
        'globs:\n'
        '  - paw-rescue/**/*\n'
        'alwaysApply: false\n'
        '---\n\n'
        '# UTF-8 \u7f16\u7801\uff08\u4e2d\u6587\u754c\u9762\u5fc5\u5b88\uff09\n\n'
        '## \u539f\u56e0\n\n'
        'Windows \u9ed8\u8ba4\u4ee3\u7801\u9875\u5e38\u4e3a GBK\u3002'
        '\u82e5 `.js` / `.py` \u4ee5 GBK \u4fdd\u5b58\uff0c\u6d4f\u89c8\u5668\u6309 UTF-8 \u89e3\u6790\u4f1a\u663e\u793a\u4e71\u7801\u3002\n\n'
        '## \u4fee\u6539\u4ee3\u7801\u65f6\n\n'
        '1. **\u7981\u6b62**\u7528\u4f1a\u6309\u7cfb\u7edf ANSI/GBK \u5199\u6587\u4ef6\u7684\u6279\u91cf\u811a\u672c\u5904\u7406\u542b\u4e2d\u6587\u7684\u6e90\u7801\u3002\n'
        '2. \u6539\u5199\u542b\u4e2d\u6587\u6587\u672c\u540e\uff0c\u5728 `paw-rescue` \u76ee\u5f55\u6267\u884c `python scripts/ensure_utf8.py`\u3002\n'
        '3. \u77ed\u5b57\u7b26\u4e32\u53ef\u7528 `\\uXXXX` \u5199\u5728 ASCII \u6e90\u6587\u4ef6\u4e2d\u3002\n'
        '4. \u5df2\u914d\u7f6e `.editorconfig`\u3001`.vscode/settings.json`\uff08`files.encoding: utf8`\uff09\u3002\n\n'
        '## \u81ea\u68c0\n\n'
        '```powershell\n'
        'python scripts/ensure_utf8.py --check\n'
        '```\n'
    )
    path.write_text(text, encoding='utf-8', newline='\n')


def main():
    fix_home(ROOT / 'frontend/src/pages/Home.js')
    fix_lostfound(ROOT / 'frontend/src/pages/LostFoundList.js')
    rule = ROOT.parent / '.cursor/rules/utf8-encoding.mdc'
    if rule.exists():
        fix_utf8_rule(rule)
    print('mojibake fix done')


if __name__ == '__main__':
    main()
