# -*- coding: utf-8 -*-
"""Patch AdminDashboard to use Chinese questionnaire labels."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / 'frontend/src/pages/AdminDashboard.js'
t = PATH.read_text(encoding='utf-8')

import_old = "import { SITE_NAME, ADOPTION_STATUS, ONLINE_STATUS, ARTICLE_TYPES } from '../constants/site';"
import_new = import_old + "\nimport getQuestionnaireEntries, { formatAttachmentType } from '../utils/adoptQuestionnaireDisplay';"
if import_new not in t:
    if import_old not in t:
        raise SystemExit('import anchor not found')
    t = t.replace(import_old, import_new, 1)

render_old = """  const renderQuestionnairePreview = (answers) => {
    if (!answers || typeof answers !== 'object') return <span className="text-muted">无问卷数据</span>;
    const entries = Object.entries(answers).slice(0, 12);
    return (
      <dl className="row mb-0 small">
        {entries.map(([key, value]) => (
          <React.Fragment key={key}>
            <dt className="col-sm-4 text-muted">{key}</dt>
            <dd className="col-sm-8">{Array.isArray(value) ? value.join('、') : String(value ?? '')}</dd>
          </React.Fragment>
        ))}
      </dl>
    );
  };"""

render_new = """  const renderQuestionnairePreview = (answers) => {
    const entries = getQuestionnaireEntries(answers);
    if (!entries.length) return <span className="text-muted">\u65e0\u95ee\u5377\u6570\u636e</span>;
    return (
      <dl className="row mb-0 small">
        {entries.map(({ key, label, value }) => (
          <React.Fragment key={key}>
            <dt className="col-sm-4 text-muted">{label}</dt>
            <dd className="col-sm-8">{value}</dd>
          </React.Fragment>
        ))}
      </dl>
    );
  };"""

if render_old not in t:
    raise SystemExit('renderQuestionnairePreview block not found')
t = t.replace(render_old, render_new, 1)

att_old = "{att.file_type || '\u9644\u4ef6'}"
att_new = "{formatAttachmentType(att.file_type)}"
if att_old in t:
    t = t.replace(att_old, att_new, 1)
else:
    # try literal Chinese in file
    att_old2 = "{att.file_type || '附件'}"
    if att_old2 in t:
        t = t.replace(att_old2, att_new, 1)

PATH.write_text(t, encoding='utf-8', newline='\n')
print('Patched AdminDashboard.js')
