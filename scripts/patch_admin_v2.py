# -*- coding: utf-8 -*-
"""Patch AdminDashboard.js - ASCII source only."""
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'frontend/src/pages/AdminDashboard.js'
text = path.read_text(encoding='utf-8')

# imports
if 'CarouselAdminPanel' not in text:
    text = text.replace(
        "import { adoptAPI, adminAPI, cmsAPI, petsAPI } from '../api/api';\n",
        "import { adoptAPI, adminAPI, cmsAPI, petsAPI } from '../api/api';\n"
        "import CarouselAdminPanel from '../components/CarouselAdminPanel';\n"
        "import CmsMarkdownEditor from '../components/CmsMarkdownEditor';\n",
    )

# ban label
if "ban:" not in text:
    text = text.replace(
        "  delete: '\u5220\u9664',\n};",
        "  delete: '\u5220\u9664',\n  ban: '\u5c01\u7981',\n};",
    )

if "value: 'user'" not in text:
    text = text.replace(
        "  { value: 'lost_found_post', label: '\u62a5\u5931\u5bfb\u4e3b' },\n];",
        "  { value: 'lost_found_post', label: '\u62a5\u5931\u5bfb\u4e3b' },\n  { value: 'user', label: '\u7528\u6237' },\n];",
    )

text = text.replace(
    "  { key: 'moderation', label: '\u5185\u5bb9\u5ba1\u6838', icon: 'fa-shield-alt' },",
    "  { key: 'moderation', label: '\u5904\u7f6e\u8bb0\u5f55', icon: 'fa-shield-alt' },\n"
    "  { key: 'carousel', label: '\u9996\u9875\u8f6e\u64ad', icon: 'fa-images' },",
)

if 'modFilter' not in text:
    text = text.replace(
        "  const [modForm, setModForm] = useState({ content_type: 'community_post', content_id: '', action: 'hide', reason: '' });\n",
        "  const [modFilter, setModFilter] = useState({ content_type: '', action: '' });\n",
    )

marker_create = "  const handleModerationCreate = async (e) => {"
marker_config = "  const handleConfigSave = async (key) => {"
if marker_create in text:
    si = text.index(marker_create)
    ei = text.index(marker_config)
    text = text[:si] + text[ei:]

# user status - match by structure with unicode in file (already utf8 from git)
text = text.replace(
    "{user.profile?.status === 1 ? '\u6b63\u5e38' : '\u7981\u7528'}",
    "{user.profile?.status === 1 ? '\u5df2\u5c01\u7981' : '\u6b63\u5e38'}",
)
text = text.replace(
    "onClick={() => handleUserUpdate(user.id, { status: 1 })}>\u542f\u7528</button>\n"
    "                  <button type=\"button\" className=\"btn btn-outline-danger\" onClick={() => handleUserUpdate(user.id, { status: 0 })}>\u7981\u7528</button>",
    "disabled={user.profile?.status !== 1} onClick={() => handleUserUpdate(user.id, { status: 0 })}>\u89e3\u5c01</button>\n"
    "                  <button type=\"button\" className=\"btn btn-outline-danger\" disabled={user.profile?.status === 1} onClick={() => handleUserUpdate(user.id, { status: 1 })}>\u5c01\u7981</button>",
)
# add disabled to first button if missing
text = text.replace(
    'className="btn btn-outline-success" onClick={() => handleUserUpdate(user.id, { status: 0 })}>\u89e3\u5c01</button>',
    'className="btn btn-outline-success" disabled={user.profile?.status !== 1} onClick={() => handleUserUpdate(user.id, { status: 0 })}>\u89e3\u5c01</button>',
)

text = text.replace(
    '<div className="col-12"><textarea className="form-control" rows={4} placeholder="\u6b63\u6587" value={articleForm.content} onChange={(e) => setArticleForm({ ...articleForm, content: e.target.value })} required /></div>',
    '<CmsMarkdownEditor value={articleForm.content} onChange={(v) => setArticleForm({ ...articleForm, content: v })} />',
)

marker_mod = "  const renderModeration = () => ("
marker_cfg = "  const renderConfig = () => ("
if 'filteredModeration' not in text:
    si = text.index(marker_mod)
    ei = text.index(marker_cfg)
    new_mod = (
        "  const filteredModeration = moderation.filter((item) => {\n"
        "    if (modFilter.content_type && item.content_type !== modFilter.content_type) return false;\n"
        "    if (modFilter.action && item.action !== modFilter.action) return false;\n"
        "    return true;\n"
        "  });\n\n"
        "  const renderModeration = () => (\n"
        "    <div>\n"
        "      <div className=\"row g-2 mb-3\">\n"
        "        <div className=\"col-md-4\">\n"
        "          <select\n"
        "            className=\"form-select form-select-sm\"\n"
        "            value={modFilter.content_type}\n"
        "            onChange={(e) => setModFilter({ ...modFilter, content_type: e.target.value })}\n"
        "          >\n"
        "            <option value=\"\">\u5168\u90e8\u5185\u5bb9\u7c7b\u578b</option>\n"
        "            {CONTENT_TYPE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}\n"
        "          </select>\n"
        "        </div>\n"
        "        <div className=\"col-md-4\">\n"
        "          <select\n"
        "            className=\"form-select form-select-sm\"\n"
        "            value={modFilter.action}\n"
        "            onChange={(e) => setModFilter({ ...modFilter, action: e.target.value })}\n"
        "          >\n"
        "            <option value=\"\">\u5168\u90e8\u64cd\u4f5c</option>\n"
        "            {Object.entries(MODERATION_ACTION_LABELS).map(([value, label]) => (\n"
        "              <option key={value} value={value}>{label}</option>\n"
        "            ))}\n"
        "          </select>\n"
        "        </div>\n"
        "      </div>\n"
        "      <p className=\"text-muted small\">\u5904\u7f6e\u8bb0\u5f55\u7531\u524d\u53f0\u7ba1\u7406\u6a21\u5f0f\u81ea\u52a8\u5199\u5165\uff0c\u6b64\u5904\u4ec5\u53ef\u67e5\u770b\u3002</p>\n"
        "      <div className=\"table-responsive\">\n"
        "        <table className=\"table table-hover\">\n"
        "          <thead>\n"
        "            <tr>\n"
        "              <th>\u65f6\u95f4</th>\n"
        "              <th>\u64cd\u4f5c\u4eba</th>\n"
        "              <th>\u5185\u5bb9\u7c7b\u578b</th>\n"
        "              <th>\u76ee\u6807</th>\n"
        "              <th>\u64cd\u4f5c</th>\n"
        "              <th>\u539f\u56e0</th>\n"
        "            </tr>\n"
        "          </thead>\n"
        "          <tbody>\n"
        "            {filteredModeration.map((item) => (\n"
        "              <tr key={item.id}>\n"
        "                <td>{new Date(item.created_at).toLocaleString()}</td>\n"
        "                <td>{item.operator?.username || '-'}</td>\n"
        "                <td>{CONTENT_TYPE_OPTIONS.find((o) => o.value === item.content_type)?.label || item.content_type}</td>\n"
        "                <td>\n"
        "                  #{item.content_id}\n"
        "                  {item.target_summary ? <small className=\"text-muted d-block\">{item.target_summary}</small> : null}\n"
        "                </td>\n"
        "                <td><span className=\"badge bg-warning text-dark\">{MODERATION_ACTION_LABELS[item.action] || item.action}</span></td>\n"
        "                <td>{item.reason || '-'}</td>\n"
        "              </tr>\n"
        "            ))}\n"
        "            {filteredModeration.length === 0 && (\n"
        "              <tr><td colSpan={6} className=\"text-muted text-center\">\u6682\u65e0\u5904\u7f6e\u8bb0\u5f55</td></tr>\n"
        "            )}\n"
        "          </tbody>\n"
        "        </table>\n"
        "      </div>\n"
        "    </div>\n"
        "  );\n\n"
    )
    text = text[:si] + new_mod + text[ei:]

if "case 'carousel'" not in text:
    text = text.replace(
        "      case 'moderation': return renderModeration();\n      case 'config': return renderConfig();",
        "      case 'moderation': return renderModeration();\n      case 'carousel': return <CarouselAdminPanel />;\n      case 'config': return renderConfig();",
    )

path.write_text(text, encoding='utf-8', newline='\n')
print('AdminDashboard patched')
