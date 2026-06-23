# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

home = ROOT / 'frontend/src/pages/Home.js'
text = home.read_text(encoding='utf-8', errors='replace')
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
text = re.sub(
    r"const PET_CATEGORIES = \[.*?\];",
    """const PET_CATEGORIES = [
  { name: '\u732b', image: catImg, link: '/pets?type=cat' },
  { name: '\u72d7', image: dogImg, link: '/pets?type=dog' },
  { name: '\u9e1f', image: birdImg, link: '/pets?type=bird' },
  { name: '\u5154', image: rabbitImg, link: '/pets?type=rabbit' },
  { name: '\u9c7c', image: fishImg, link: '/pets?type=fish' },
];""",
    text,
    count=1,
    flags=re.S,
)
replacements = [
    ("return '\u6b22\u8fce\u9886\u517b'", "return '\u6b22\u8fce\u9886\u517b'"),
    ("alt={item.title || '\u8f6e\u64ad\u56fe'}", "alt={item.title || '\u8f6e\u64ad\u56fe'}"),
]
# bulk replace known broken phrases via regex
fixes = [
    (r"aria-label=\{`[^`]*`\}", "aria-label={`\u7b2c ${index + 1} \u5f20`}"),
    (r"alt=\{item\.title \|\| '[^']*'\}", "alt={item.title || '\u8f6e\u64ad\u56fe'}"),
    (r"<span className=\"visually-hidden\">[^<]*</span>\s*\n\s*</button>\s*\n\s*<button className=\"carousel-control-next\"", "<span className=\"visually-hidden\">\u4e0a\u4e00\u5f20</span>\n          </button>\n          <button className=\"carousel-control-next\""),
]
# simpler string replacements for dashboard section
subs = {
    '\u6700\u65b0\u52a8\u6001': '\u6700\u65b0\u52a8\u6001',
}
for old, new in [
    ('\u52a8\u6001\u52a0\u8f7d\u5931\u8d25', '\u52a8\u6001\u52a0\u8f7d\u5931\u8d25'),
    ('\u6700\u65b0\u516c\u544a', '\u6700\u65b0\u516c\u544a'),
    ('\u7d27\u6025\u5bfb\u4e3b', '\u7d27\u6025\u5bfb\u4e3b'),
    ('\u79d1\u666e\u6587\u7ae0', '\u79d1\u666e\u6587\u7ae0'),
    ('\u6700\u65b0\u52a8\u6001', '\u6700\u65b0\u52a8\u6001'),
    ('\u52a0\u8f7d\u6700\u65b0\u52a8\u6001', '\u52a0\u8f7d\u6700\u65b0\u52a8\u6001'),
    ('\u4e0a\u4e00\u5f20', '\u4e0a\u4e00\u5f20'),
    ('\u4e0b\u4e00\u5f20', '\u4e0b\u4e00\u5f20'),
    ('\u8f6e\u64ad\u56fe', '\u8f6e\u64ad\u56fe'),
    ('\u5e73\u53f0\u6570\u636e\u6982\u89c8', '\u5e73\u53f0\u6570\u636e\u6982\u89c8'),
]:
    pass
# replace any line containing replacement char sequences - use targeted regex for dashboard headings
text = re.sub(r'>\s*[^<\n]{0,20}\u52a8\u6001[^<]{0,10}<', '>\u6700\u65b0\u52a8\u6001<', text)
text = re.sub(r'加载[^<]{0,12}\.\.\.', '\u52a0\u8f7d\u6700\u65b0\u52a8\u6001...', text, count=1)
text = re.sub(r'动态[^<]{0,8}加载失败', '\u52a8\u6001\u52a0\u8f7d\u5931\u8d25', text, count=1)
text = re.sub(r"item\.title \|\| '[^']*'", "item.title || '\u8f6e\u64ad\u56fe'", text)
text = re.sub(r'aria-label=\{`[^`]+`\}', "aria-label={`\u7b2c ${index + 1} \u5f20`}", text)
text = re.sub(r'<span className="visually-hidden">上一[^<]*</span>', '<span className="visually-hidden">\u4e0a\u4e00\u5f20</span>', text)
text = re.sub(r'<span className="visually-hidden">下一[^<]*</span>', '<span className="visually-hidden">\u4e0b\u4e00\u5f20</span>', text)
text = re.sub(r'紧急[^<]{0,6}寻[^<]*', '\u7d27\u6025\u5bfb\u4e3b', text, count=1)
text = re.sub(r'>最新[^<]{0,6}公告<', '>\u6700\u65b0\u516c\u544a<', text, count=1)
home.write_text(text, encoding='utf-8', newline='\n')

lf = ROOT / 'frontend/src/pages/LostFoundList.js'
t = lf.read_text(encoding='utf-8', errors='replace')
t = re.sub(r"\{ key: '', label: '[^']*' \}", "{ key: '', label: '\u5168\u90e8\u72b6\u6001' }", t, count=1)
t = t.replace('\ufffd', '')
t = re.sub(r'悬赏 \{post\.reward_amount\} [^\n]+', '悬赏 \u00a5{post.reward_amount}', t, count=1)
t = re.sub(r"setError\('加载信息失败[^']*'\)", "setError('\u52a0\u8f7d\u4fe1\u606f\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5\u3002')", t, count=1)
lf.write_text(t, encoding='utf-8', newline='\n')
print('home/lf fixed')
