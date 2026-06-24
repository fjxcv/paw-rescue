# -*- coding: utf-8 -*-
import os
import re

path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'pages', 'Home.js')
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

helper = """
  const normalizeCarouselTitle = (title) => {
    if (!title) return '';
    const t = String(title).trim();
    if (/welcome\\s*to\\s*adoption/i.test(t)) return '\\u6b22\\u8fce\\u9886\\u517b';
    return t;
  };
""".replace('\\u6b22\\u8fce\\u9886\\u517b', '\u6b22\u8fce\u9886\u517b')

if 'normalizeCarouselTitle' not in text:
    text = text.replace(
        '  useEffect(() => {\n    const fetchCarousel',
        helper + '\n  useEffect(() => {\n    const fetchCarousel',
    )

text = re.sub(
    r"setCarouselItems\(response\.data\);",
    "setCarouselItems((response.data || []).map((item) => ({ ...item, title: normalizeCarouselTitle(item.title) })));",
    text,
    count=1,
)

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print('patched Home.js')
