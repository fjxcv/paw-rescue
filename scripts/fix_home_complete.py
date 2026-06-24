# -*- coding: utf-8 -*-
"""Fix Home.js mojibake - ASCII source only."""
import re
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'frontend/src/pages/Home.js'
text = path.read_text(encoding='utf-8', errors='replace')

text = re.sub(
    r"const STATS_CONFIG = \[.*?\];",
    """const STATS_CONFIG = [
  { key: 'total_rescued', label: '\u7d2f\u8ba1\u6551\u52a9', icon: 'fa-check-circle', color: 'success' },
  { key: 'total_adopted', label: '\u7d2f\u8ba1\u9886\u517b', icon: 'fa-home', color: 'primary' },
  { key: 'searching_count', label: '\u6b63\u5728\u5bfb\u627e', icon: 'fa-search', color: 'danger' },
  { key: 'today_reported', label: '\u4eca\u65e5\u4e0a\u62a5', icon: 'fa-flag', color: 'warning' },
];""",
    text,
    count=1,
    flags=re.S,
)

def sub(pattern, repl_fn, s, count=0):
    return re.sub(pattern, lambda m: repl_fn(m), s, count=count)

text = sub(
    r"if \(/welcome\\s\*to\\s\*adoption/i\.test\(t\)\) return '[^']*';",
    lambda _m: "if (/welcome\\s*to\\s*adoption/i.test(t)) return '\u6b22\u8fce\u9886\u517b';",
    text,
    1,
)
text = sub(r"aria-label=\{`[^`]*`\}", lambda _m: "aria-label={`\u7b2c ${index + 1} \u5f20`}", text, 1)
text = re.sub(r"item\.title \|\| '[^']*'", "item.title || '\u8f6e\u64ad\u56fe'", text)
text = sub(
    r'<span className="visually-hidden">[^<]*</span>\s*\n\s*</button>\s*\n\s*<button className="carousel-control-next"',
    lambda _m: '<span className="visually-hidden">\u4e0a\u4e00\u5f20</span>\n          </button>\n          <button className="carousel-control-next"',
    text,
    1,
)
text = sub(
    r'(<button className="carousel-control-next"[^>]*>\s*<span className="carousel-control-next-icon"[^/]*/>\s*)<span className="visually-hidden">[^<]*</span>',
    lambda m: m.group(1) + '<span className="visually-hidden">\u4e0b\u4e00\u5f20</span>',
    text,
    1,
)
text = sub(
    r'(<i className="fas fa-chart-bar me-2 text-success"></i>\s*)[^\n<]+',
    lambda m: m.group(1) + '\u5e73\u53f0\u6570\u636e\u6982\u89c8',
    text,
    1,
)
text = sub(
    r'(<span className="ms-2 text-muted small">)[^<]+(</span>\s*\n\s*</div>\s*\) : statsError)',
    lambda m: m.group(1) + '\u52a0\u8f7d\u7edf\u8ba1\u6570\u636e...' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<span className="text-muted small">)[^<]+(</span>\s*\n\s*<button className="btn btn-sm btn-outline-secondary ms-2" onClick=\{fetchStats\})',
    lambda m: m.group(1) + '\u7edf\u8ba1\u6570\u636e\u52a0\u8f7d\u5931\u8d25' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<i className="fas fa-redo me-1"></i>)[^<]+(</button>\s*\n\s*</div>\s*\) : stats)',
    lambda m: m.group(1) + '\u91cd\u8bd5' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<i className="fas fa-bolt me-2 text-warning"></i>\s*)[^\n<]+',
    lambda m: m.group(1) + '\u6700\u65b0\u52a8\u6001',
    text,
    1,
)
text = sub(
    r'(<span className="ms-2 text-muted small">)[^<]+(</span>\s*\n\s*</div>\s*\) : dashboardError)',
    lambda m: m.group(1) + '\u52a0\u8f7d\u6700\u65b0\u52a8\u6001...' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<span className="text-muted small">)[^<]+(</span>\s*\n\s*<button className="btn btn-sm btn-outline-secondary ms-2" onClick=\{fetchDashboard\})',
    lambda m: m.group(1) + '\u52a8\u6001\u52a0\u8f7d\u5931\u8d25' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<i className="fas fa-redo me-1"></i>)[^<]+(</button>\s*\n\s*</div>\s*\) : dashboard)',
    lambda m: m.group(1) + '\u91cd\u65b0\u52a0\u8f7d' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<i className="fas fa-exclamation-triangle me-2"></i>)[^\n<]+',
    lambda m: m.group(1) + '\u7d27\u6025\u5bfb\u4e3b',
    text,
    1,
)
text = sub(
    r'(<span className="badge bg-warning text-dark ms-1">)[^<]+(\{item\.reward_amount\})',
    lambda m: m.group(1) + '\u60a9\u8d4f \u00a5' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<p className="text-muted small mb-0">)[^<]+(</p>\s*\n\s*<Link to="/lost-found")',
    lambda m: m.group(1) + '\u6682\u65e0\u62a5\u5931\u4fe1\u606f' + m.group(2),
    text,
    1,
)
text = sub(
    r'(to="/lost-found"[^>]*>\s*)[^\n<]+(<i className="fas fa-arrow-right)',
    lambda m: m.group(1) + '\u67e5\u770b\u5168\u90e8 ' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<i className="fas fa-bullhorn me-2"></i>)[^\n<]+',
    lambda m: m.group(1) + '\u6700\u65b0\u516c\u544a',
    text,
    1,
)
text = sub(
    r'(<p className="text-muted small mb-0">)[^<]+(</p>\s*\n\s*<Link to="/cms\?type=announcement")',
    lambda m: m.group(1) + '\u6682\u65e0\u516c\u544a' + m.group(2),
    text,
    1,
)
text = sub(
    r'(to="/cms\?type=announcement"[^>]*>\s*)[^\n<]+(<i className="fas fa-arrow-right)',
    lambda m: m.group(1) + '\u67e5\u770b\u5168\u90e8\u516c\u544a ' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<Link to="/cms\?type=science"[^>]*>\s*)[^\n<]+(<i className="fas fa-arrow-right)',
    lambda m: m.group(1) + '\u67e5\u770b\u66f4\u591a ' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<h4 className="card-title"><i className="fas fa-robot me-2 text-success" />)AI [^<]+(</h4>)',
    lambda m: m.group(1) + 'AI \u54c1\u79cd\u8bc6\u522b' + m.group(2),
    text,
    1,
)
text = sub(
    r'(<p className="text-muted small">)[^<]+(</p>\s*\n\s*<form)',
    lambda m: m.group(1) + '\u4e0a\u4f20\u5ba0\u7269\u7167\u7247\u540e\uff0c\u5c06\u4f7f\u7528\u57fa\u4e8e Oxford-IIIT Pet \u7b49\u516c\u5f00\u6570\u636e\u96c6\u8bad\u7ec3\u7684\u672c\u5730 CNN \u6a21\u578b\u8bc6\u522b\u54c1\u79cd\uff08Top \u5019\u9009\u4e0e\u7f6e\u4fe1\u5ea6\uff09\u3002' + m.group(2),
    text,
    1,
)
text = re.sub(
    r'placeholder="[^"]*"',
    "placeholder=\"\u5982\uff1a\u6a59\u8272\u77ed\u6bdb\u3001\u7eff\u773c\u775b\"",
    text,
    count=1,
)
text = re.sub(
    r"\{aiLoading \? '[^']*' : '[^']*'\}",
    "{aiLoading ? '\u8bc6\u522b\u4e2d...' : '\u5f00\u59cb\u8bc6\u522b'}",
    text,
    count=1,
)
text = sub(
    r'(<h3 className="text-center mb-5">)[^<]+(</h3>)',
    lambda m: m.group(1) + '\u6d4f\u89c8\u5ba0\u7269\u5206\u7c7b' + m.group(2),
    text,
    1,
)

path.write_text(text, encoding='utf-8', newline='\n')
print('Home.js fixed')
