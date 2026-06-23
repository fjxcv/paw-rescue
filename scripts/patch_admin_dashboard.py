# -*- coding: utf-8 -*-
"""Patch AdminDashboard.js using ASCII-only source + unicode escapes."""
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'frontend/src/pages/AdminDashboard.js'
text = path.read_text(encoding='utf-8')

# imports
old_imp = "import { adoptAPI, adminAPI, cmsAPI, petsAPI } from '../api/api';"
new_imp = (
    "import { adoptAPI, adminAPI, cmsAPI, petsAPI } from '../api/api';\n"
    "import CmsMarkdownEditor from '../components/CmsMarkdownEditor';\n"
    "import CarouselAdminPanel from '../components/CmsMarkdownEditor';\n"
)
# fix carousel import path
new_imp = (
    "import { adoptAPI, adminAPI, cmsAPI, petsAPI } from '../api/api';\n"
    "import CmsMarkdownEditor from '../components/CmsMarkdownEditor';\n"
    "import CarouselAdminPanel from '../components/CarouselAdminPanel';"
)
if 'CmsMarkdownEditor' not in text:
    text = text.replace(old_imp, new_imp)

# labels
text = text.replace(
    "const MODERATION_ACTION_LABELS = {\n  approve: '\u901a\u8fc7',\n  hide: '\u9690\u85cf',\n  delete: '\u5220\u9664',\n};",
    "const MODERATION_ACTION_LABELS = {\n  approve: '\u901a\u8fc7',\n  hide: '\u9690\u85cf',\n  delete: '\u5220\u9664',\n  ban: '\u5c01\u7981',\n};",
)
if "ban: '\u5c01\u7981'" not in text:
    text = text.replace(
        "  delete: '\u5220\u9664',\n};",
        "  delete: '\u5220\u9664',\n  ban: '\u5c01\u7981',\n};",
    )

if "value: 'user'" not in text:
    text = text.replace(
        "  { value: 'lost_found_post', label: '\u62a5\u5931\u5bfb\u4e3b' },\n];",
        "  { value: 'lost_found_post', label: '\u62a5\u5931\u5bfb\u4e3b' },\n  { value: 'user', label: '\u7528\u6237' },\n];",
    )

# tabs
text = text.replace(
    "  { key: 'moderation', label: '\u5185\u5bb9\u5ba1\u6838', icon: 'fa-shield-alt' },",
    "  { key: 'moderation', label: '\u5904\u7f6e\u8bb0\u5f55', icon: 'fa-shield-alt' },\n  { key: 'carousel', label: '\u9996\u9875\u8f6e\u64ad', icon: 'fa-images' },",
)

# remove modForm state, add modFilter
if 'modFilter' not in text:
    text = text.replace(
        "  const [modForm, setModForm] = useState({ content_type: 'community_post', content_id: '', action: 'hide', reason: '' });\n",
        "  const [modFilter, setModFilter] = useState({ content_type: '', action: '' });\n",
    )

# remove handleModerationCreate
start = text.find('  const handleModerationCreate = async (e) => {')
if start != -1:
    end = text.find('  const handleConfigSave = async (key) => {', start)
    if end != -1:
        text = text[:start] + text[end:]

# fix users status
text = text.replace(
    "<td>{user.profile?.status === 1 ? '\u6b63\u5e38' : '\u7981\u7528'}</td>",
    "<td>{user.profile?.status === 1 ? '\u5df2\u5c01\u7981' : '\u6b63\u5e38'}</td>",
)
text = text.replace(
    "<button type=\"button\" className=\"btn btn-outline-success\" onClick={() => handleUserUpdate(user.id, { status: 1 })}>\u542f\u7528</button>\n                  <button type=\"button\" className=\"btn btn-outline-danger\" onClick={() => handleUserUpdate(user.id, { status: 0 })}>\u7981\u7528</button>",
    "<button type=\"button\" className=\"btn btn-outline-success\" disabled={user.profile?.status !== 1} onClick={() => handleUserUpdate(user.id, { status: 0 })}>\u89e3\u5c01</button>\n                  <button type=\"button\" className=\"btn btn-outline-danger\" disabled={user.profile?.status === 1} onClick={() => handleUserUpdate(user.id, { status: 1 })}>\u5c01\u7981</button>",
)

# cms markdown editor
old_ta = (
    '            <div className="col-12"><textarea className="form-control" rows={4} placeholder="\u6b63\u6587" value={articleForm.content} onChange={(e) => setArticleForm({ ...articleForm, content: e.target.value })} required /></div>\n'
)
new_ta = (
    '            <CmsMarkdownEditor value={articleForm.content} onChange={(v) => setArticleForm({ ...articleForm, content: v })} />\n'
)
if 'CmsMarkdownEditor' in text and '<CmsMarkdownEditor' not in text:
    text = text.replace(old_ta, new_ta)

# replace renderModeration block
old_mod_start = '  const renderModeration = () => ('
old_mod_end = '  const renderConfig = () => ('
si = text.find(old_mod_start)
ei = text.find(old_mod_end)
if si != -1 and ei != -1:
    new_mod = r'''  const filteredModeration = moderation.filter((item) => {
    if (modFilter.content_type && item.content_type !== modFilter.content_type) return false;
    if (modFilter.action && item.action !== modFilter.action) return false;
    return true;
  });

  const renderModeration = () => (
    <div>
      <div className="row g-2 mb-3">
        <div className="col-md-4">
          <select
            className="form-select form-select-sm"
            value={modFilter.content_type}
            onChange={(e) => setModFilter({ ...modFilter, content_type: e.target.value })}
          >
            <option value="">全部内容类型</option>
            {CONTENT_TYPE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </div>
        <div className="col-md-4">
          <select
            className="form-select form-select-sm"
            value={modFilter.action}
            onChange={(e) => setModFilter({ ...modFilter, action: e.target.value })}
          >
            <option value="">全部操作</option>
            {Object.entries(MODERATION_ACTION_LABELS).map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
        </div>
      </div>
      <p className="text-muted small">处置记录由前台管理模式自动写入，此处仅可查看。</p>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th>时间</th>
              <th>操作人</th>
              <th>内容类型</th>
              <th>目标</th>
              <th>操作</th>
              <th>原因</th>
            </tr>
          </thead>
          <tbody>
            {filteredModeration.map((item) => (
              <tr key={item.id}>
                <td>{new Date(item.created_at).toLocaleString()}</td>
                <td>{item.operator?.username || '-'}</td>
                <td>{CONTENT_TYPE_OPTIONS.find((o) => o.value === item.content_type)?.label || item.content_type}</td>
                <td>
                  #{item.content_id}
                  {item.target_summary ? <small className="text-muted d-block">{item.target_summary}</small> : null}
                </td>
                <td><span className="badge bg-warning text-dark">{MODERATION_ACTION_LABELS[item.action] || item.action}</span></td>
                <td>{item.reason || '-'}</td>
              </tr>
            ))}
            {filteredModeration.length === 0 && (
              <tr><td colSpan={6} className="text-muted text-center">暂无处置记录</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );

'''
    text = text[:si] + new_mod + text[ei:]

# renderTabContent carousel
if "case 'carousel'" not in text:
    text = text.replace(
        "      case 'moderation': return renderModeration();\n      case 'config': return renderConfig();",
        "      case 'moderation': return renderModeration();\n      case 'carousel': return <CarouselAdminPanel />;\n      case 'config': return renderConfig();",
    )

path.write_text(text, encoding='utf-8', newline='\n')
print('AdminDashboard patched OK')
