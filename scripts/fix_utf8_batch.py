# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Fix Home.js PET_CATEGORIES pet names
home = ROOT / 'frontend/src/pages/Home.js'
text = home.read_text(encoding='utf-8')
text = text.replace(
    "const PET_CATEGORIES = [\n  { name: '\u732b', image: catImg, link: '/pets?type=cat' },",
    "const PET_CATEGORIES = [\n  { name: '\u732b', image: catImg, link: '/pets?type=cat' },",
)
# Replace broken pet category block entirely
import re
text = re.sub(
    r"const PET_CATEGORIES = \[.*?\];",
    """const PET_CATEGORIES = [
  { name: '\\u732b', image: catImg, link: '/pets?type=cat' },
  { name: '\\u72d7', image: dogImg, link: '/pets?type=dog' },
  { name: '\\u9e1f', image: birdImg, link: '/pets?type=bird' },
  { name: '\\u5154', image: rabbitImg, link: '/pets?type=rabbit' },
  { name: '\\u9c7c', image: fishImg, link: '/pets?type=fish' },
];""",
    text,
    count=1,
    flags=re.S,
)
# Fix escaped unicode in JS - need actual chars not \\u in output
text = text.replace("'\\u732b'", "'\u732b'").replace("'\\u72d7'", "'\u72d7'")
text = text.replace("'\\u9e1f'", "'\u9e1f'").replace("'\\u5154'", "'\u5154'").replace("'\\u9c7c'", "'\u9c7c'")
home.write_text(text, encoding='utf-8', newline='\n')

# LostFoundList status tab
lf = ROOT / 'frontend/src/pages/LostFoundList.js'
t = lf.read_text(encoding='utf-8', errors='replace')
t = re.sub(
    r"\{ key: '', label: '[^']*' \}",
    lambda _m: "{ key: '', label: '\u5168\u90e8\u72b6\u6001' }",
    t,
    count=1,
)
# fix other broken strings in LostFoundList
replacements = [
    (r"ÐüÉÍ \{post\.reward_amount\} [^\n]+", "ÐüÉÍ \u00a5{post.reward_amount}"),
    (r"alert\('ÒÑ·â[^']*'\)", "alert('\u5df2\u5c01\u7981')"),
]
for pat, rep in replacements:
    t = re.sub(pat, rep, t, count=1)
lf.write_text(t, encoding='utf-8', newline='\n')

print('utf8 batch done')
