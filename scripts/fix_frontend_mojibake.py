# -*- coding: utf-8 -*-
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent

lf = root / 'frontend' / 'src' / 'pages' / 'LostFoundList.js'
text = lf.read_text(encoding='utf-8')
text = re.sub(
    r"attribution: '&copy; [^']*'",
    lambda _m: "attribution: '" + "\u00a9 \u9ad8\u5fb7\u5730\u56fe" + "'",
    text,
    count=1,
)
text = re.sub(
    r"\{nearbyLoading \? '[^']*' : '[^']*'\}",
    lambda _m: "{nearbyLoading ? '\u5b9a\u4f4d\u4e2d...' : '\u9644\u8fd1\u641c\u7d22'}",
    text,
    count=1,
)
lf.write_text(text, encoding='utf-8', newline='\n')

pd = root / 'frontend' / 'src' / 'pages' / 'PetDetail.js'
text = pd.read_text(encoding='utf-8')
text = re.sub(
    r"const QUESTIONNAIRE_FIELDS = \[.*?\];",
    """const QUESTIONNAIRE_FIELDS = [
  { key: 'housing_type', label: '\u5c45\u4f4f\u7c7b\u578b\uff08\u516c\u5bd3/\u72ec\u680b/\u5176\u4ed6\uff09' },
  { key: 'has_other_pets', label: '\u662f\u5426\u5df2\u6709\u5176\u4ed6\u5ba0\u7269\uff1f\uff08\u662f/\u5426\uff09' },
  { key: 'experience', label: '\u517b\u5ba0\u7ecf\u9a8c' },
  { key: 'daily_hours', label: '\u6bcf\u65e5\u5728\u5bb6\u65f6\u957f\uff08\u5c0f\u65f6\uff09' },
  { key: 'family_agreement', label: '\u5bb6\u4eba\u662f\u5426\u540c\u610f\u9886\u517b\uff1f\uff08\u662f/\u5426\uff09' },
];""",
    text,
    count=1,
    flags=re.S,
)
text = re.sub(
    r"const FILE_TYPE_LABELS = \{.*?\};",
    """const FILE_TYPE_LABELS = {
  id_card: '\u8eab\u4efd\u8bc1',
  income_proof: '\u6536\u5165\u8bc1\u660e',
  housing_proof: '\u4f4f\u623f\u8bc1\u660e',
  other: '\u5176\u4ed6',
};""",
    text,
    count=1,
    flags=re.S,
)
text = re.sub(
    r"return user\.username \|\| user\.name \|\| '[^']*';",
    "return user.username || user.name || '\u8bbf\u5ba2';",
    text,
    count=1,
)
pd.write_text(text, encoding='utf-8', newline='\n')
print('done')
