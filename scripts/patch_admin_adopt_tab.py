# -*- coding: utf-8 -*-
"""Patch AdminDashboard adopt tab and adopt.js for admin list + review detail."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ADOPT_JS = ROOT / 'frontend/src/api/adopt.js'
text = ADOPT_JS.read_text(encoding='utf-8')
old = "  getAll: () => api.get('/adopt/applications/'),"
new = "  getAll: () => api.get('/adopt/applications/admin/'),\n  getAllLegacy: () => api.get('/adopt/applications/'),"
if old not in text:
    raise SystemExit('adopt.js getAll line not found')
ADOPT_JS.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')

ADMIN = ROOT / 'frontend/src/pages/AdminDashboard.js'
t = ADMIN.read_text(encoding='utf-8')

state_old = "  const [showArticleForm, setShowArticleForm] = useState(false);"
state_new = state_old + """
  const [reviewDetail, setReviewDetail] = useState(null);
  const [reviewLoadingId, setReviewLoadingId] = useState(null);"""
if state_old not in t:
    raise SystemExit('AdminDashboard state anchor not found')
t = t.replace(state_old, state_new, 1)

handler_old = """  const handleAudit = async (appId) => {
    const form = auditForm[appId] || { online_status: 'approved', audit_opinion: '' };
    try {
      await adoptAPI.audit(appId, form);
      loadTabData('adopt');
    } catch (err) {
      alert('\u5ba1\u6838\u5931\u8d25');
      console.error(err);
    }
  };"""
handler_new = """  const loadReviewDetail = async (appId) => {
    if (reviewDetail?.id === appId) {
      setReviewDetail(null);
      return;
    }
    setReviewLoadingId(appId);
    try {
      const res = await adoptAPI.getReviewDetail(appId);
      setReviewDetail(res.data);
    } catch (err) {
      alert(getApiError(err) || '\u52a0\u8f7d\u7533\u8bf7\u8be6\u60c5\u5931\u8d25');
      console.error(err);
    } finally {
      setReviewLoadingId(null);
    }
  };

  const handleAudit = async (appId) => {
    const form = auditForm[appId] || { online_status: 'approved', audit_opinion: '' };
    if (!form.online_status) {
      alert('\u8bf7\u9009\u62e9\u5ba1\u6838\u7ed3\u679c');
      return;
    }
    try {
      await adoptAPI.audit(appId, form);
      setReviewDetail(null);
      loadTabData('adopt');
    } catch (err) {
      alert(getApiError(err) || '\u5ba1\u6838\u5931\u8d25');
      console.error(err);
    }
  };"""
if handler_old not in t:
    raise SystemExit('handleAudit block not found')
t = t.replace(handler_old, handler_new, 1)

render_old = """  const renderAdoptAudit = () => (
    <div className="table-responsive">
      <table className="table table-hover">
        <thead>
          <tr>
            <th>\u7533\u8bf7\u4eba</th>
            <th>\u5ba0\u7269</th>
            <th>\u7559\u8a00</th>
            <th>\u72b6\u6001</th>
            <th>\u5ba1\u6838</th>
          </tr>
        </thead>
        <tbody>
          {applications.map((app) => (
            <tr key={app.id}>
              <td>{app.applicant?.username}</td>
              <td>{app.pet?.name || app.pet_id}</td>
              <td style={{ maxWidth: 150 }}>{app.message}</td>
              <td><span className="badge bg-secondary">{ONLINE_STATUS[app.online_status] || app.online_status}</span></td>
              <td>
                {app.online_status === 'pending' ? (
                  <div className="d-flex flex-column gap-1" style={{ minWidth: 200 }}>
                    <select
                      className="form-select form-select-sm"
                      value={auditForm[app.id]?.online_status || 'approved'}
                      onChange={(e) => setAuditForm({ ...auditForm, [app.id]: { ...auditForm[app.id], online_status: e.target.value } })}
                    >
                      <option value="approved">\u901a\u8fc7</option>
                      <option value="rejected">\u62d2\u7edd</option>
                      <option value="need_material">\u9700\u8865\u6750\u6599</option>
                    </select>
                    <input
                      type="text"
                      className="form-control form-control-sm"
                      placeholder="\u5ba1\u6838\u610f\u89c1"
                      value={auditForm[app.id]?.audit_opinion || ''}
                      onChange={(e) => setAuditForm({ ...auditForm, [app.id]: { ...auditForm[app.id], audit_opinion: e.target.value } })}
                    />
                    <button type="button" className="btn btn-success btn-sm" onClick={() => handleAudit(app.id)}>\u63d0\u4ea4\u5ba1\u6838</button>
                  </div>
                ) : (
                  <small className="text-muted">{app.audit_opinion || '\u5df2\u5ba1\u6838'}</small>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );"""

render_new = """  const renderQuestionnairePreview = (answers) => {
    if (!answers || typeof answers !== 'object') return <span className="text-muted">\u65e0\u95ee\u5377\u6570\u636e</span>;
    const entries = Object.entries(answers).slice(0, 12);
    return (
      <dl className="row mb-0 small">
        {entries.map(([key, value]) => (
          <React.Fragment key={key}>
            <dt className="col-sm-4 text-muted">{key}</dt>
            <dd className="col-sm-8">{Array.isArray(value) ? value.join('\u3001') : String(value ?? '')}</dd>
          </React.Fragment>
        ))}
      </dl>
    );
  };

  const renderAdoptAudit = () => (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <p className="text-muted small mb-0">\u5171 {applications.length} \u6761\u7533\u8bf7\uff0c\u70b9\u51fb\u300c\u67e5\u770b\u8be6\u60c5\u300d\u53ef\u67e5\u770b\u95ee\u5377\u4e0e\u9644\u4ef6\u3002</p>
        <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => loadTabData('adopt')}>
          <i className="fas fa-redo me-1"></i>\u5237\u65b0
        </button>
      </div>
      {applications.length === 0 ? (
        <div className="alert alert-light text-center mb-0">\u6682\u65e0\u9886\u517b\u7533\u8bf7\u8bb0\u5f55</div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead>
              <tr>
                <th>ID</th>
                <th>\u7533\u8bf7\u4eba</th>
                <th>\u5ba0\u7269</th>
                <th>\u7559\u8a00</th>
                <th>\u6750\u6599</th>
                <th>\u72b6\u6001</th>
                <th>\u7533\u8bf7\u65f6\u95f4</th>
                <th>\u64cd\u4f5c</th>
              </tr>
            </thead>
            <tbody>
              {applications.map((app) => (
                <tr key={app.id}>
                  <td>{app.id}</td>
                  <td>{app.applicant?.username}</td>
                  <td>{app.pet?.name || app.pet_id}</td>
                  <td style={{ maxWidth: 140 }} className="text-truncate" title={app.message}>{app.message || '-'}</td>
                  <td>
                    {app.has_questionnaire ? <span className="badge bg-info text-dark me-1">\u95ee\u5377</span> : null}
                    {(app.attachment_count || 0) > 0 ? <span className="badge bg-secondary">\u9644\u4ef6 {app.attachment_count}</span> : null}
                    {!app.has_questionnaire && !(app.attachment_count > 0) ? <span className="text-muted small">\u5f85\u8865\u5145</span> : null}
                  </td>
                  <td><span className="badge bg-secondary">{ONLINE_STATUS[app.online_status] || app.online_status}</span></td>
                  <td><small>{app.created_at ? new Date(app.created_at).toLocaleString() : '-'}</small></td>
                  <td>
                    <button
                      type="button"
                      className="btn btn-outline-primary btn-sm mb-1"
                      onClick={() => loadReviewDetail(app.id)}
                      disabled={reviewLoadingId === app.id}
                    >
                      {reviewLoadingId === app.id ? '\u52a0\u8f7d\u4e2d...' : (reviewDetail?.id === app.id ? '\u6536\u8d77\u8be6\u60c5' : '\u67e5\u770b\u8be6\u60c5')}
                    </button>
                    {app.online_status === 'pending' ? (
                      <div className="d-flex flex-column gap-1 mt-1" style={{ minWidth: 200 }}>
                        <select
                          className="form-select form-select-sm"
                          value={auditForm[app.id]?.online_status || 'approved'}
                          onChange={(e) => setAuditForm({ ...auditForm, [app.id]: { ...auditForm[app.id], online_status: e.target.value } })}
                        >
                          <option value="approved">\u901a\u8fc7</option>
                          <option value="rejected">\u62d2\u7edd</option>
                          <option value="need_material">\u9700\u8865\u6750\u6599</option>
                        </select>
                        <input
                          type="text"
                          className="form-control form-control-sm"
                          placeholder="\u5ba1\u6838\u610f\u89c1"
                          value={auditForm[app.id]?.audit_opinion || ''}
                          onChange={(e) => setAuditForm({ ...auditForm, [app.id]: { ...auditForm[app.id], audit_opinion: e.target.value } })}
                        />
                        <button type="button" className="btn btn-success btn-sm" onClick={() => handleAudit(app.id)}>\u63d0\u4ea4\u5ba1\u6838</button>
                      </div>
                    ) : (
                      <small className="text-muted d-block">{app.audit_opinion || '\u5df2\u5ba1\u6838'}</small>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {reviewDetail && (
        <div className="card mt-3 border-primary">
          <div className="card-header d-flex justify-content-between align-items-center">
            <span>\u7533\u8bf7 #{reviewDetail.id} \u8be6\u60c5</span>
            <button type="button" className="btn-close" aria-label="\u5173\u95ed" onClick={() => setReviewDetail(null)} />
          </div>
          <div className="card-body">
            <p className="mb-2"><strong>\u7533\u8bf7\u4eba\uff1a</strong>{reviewDetail.applicant?.username} {reviewDetail.applicant_phone_masked ? `\uff08${reviewDetail.applicant_phone_masked}\uff09` : ''}</p>
            <p className="mb-2"><strong>\u5ba0\u7269\uff1a</strong>{reviewDetail.pet?.name || '-'}</p>
            <p className="mb-3"><strong>\u7559\u8a00\uff1a</strong>{reviewDetail.message || '-'}</p>
            <h6>\u95ee\u5377\u56de\u7b54</h6>
            <div className="mb-3">{renderQuestionnairePreview(reviewDetail.questionnaire)}</div>
            <h6>\u9644\u4ef6</h6>
            {reviewDetail.attachments?.length ? (
              <ul className="list-unstyled mb-0">
                {reviewDetail.attachments.map((att) => (
                  <li key={att.id} className="mb-1">
                    <a href={att.file_url} target="_blank" rel="noopener noreferrer">{att.file_type || '\u9644\u4ef6'}</a>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-muted small mb-0">\u6682\u65e0\u9644\u4ef6</p>
            )}
          </div>
        </div>
      )}
    </div>
  );"""

# Match renderAdoptAudit using regex since file may have UTF-8 Chinese already
import re
pat = r"  const renderAdoptAudit = \(\) => \(\s*<div className=\"table-responsive\">[\s\S]*?\n  \);"
if not re.search(pat, t):
    raise SystemExit('renderAdoptAudit block not found')
t = re.sub(pat, render_new, t, count=1)

ADMIN.write_text(t, encoding='utf-8', newline='\n')
print('Patched adopt.js and AdminDashboard.js')
