# -*- coding: utf-8 -*-
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'frontend/src/pages/Home.js'
text = path.read_text(encoding='utf-8')
text = text.replace(
    "    if (/welcome\\s*to\\s*adoption/i.test(t)) return '\u5a07\u4e32\u7e41\u5b57\u4e71\u7801';",
    "    if (/welcome\\s*to\\s*adoption/i.test(t)) return '\u6b22\u8fce\u9886\u517b';",
)
# also fix literal mojibake if present
text = text.replace(
    "return '\u5a07\u4e32\u7e41\u5b57\u4e71\u7801';",
    "return '\u6b22\u8fce\u9886\u517b';",
)
# fix known bad string
text = text.replace(
    "return '\u5a07\u4e32\u7e41\u5b57\u4e71\u7801';",
    "return '\u6b22\u8fce\u9886\u517b';",
)
if '娆' in text or '繋' in text:
    import re
    text = re.sub(
        r"return '[^']*';(\s*\n\s*return t;)",
        "return '\u6b22\u8fce\u9886\u517b';\\1",
        text,
        count=1,
    )

path.write_text(text, encoding='utf-8', newline='\n')
print('Home normalize patched')
