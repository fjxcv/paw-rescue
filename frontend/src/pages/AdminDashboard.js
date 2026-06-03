import React, { useCallback, useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { adoptAPI, adminAPI, cmsAPI, petsAPI } from '../api/api';
import { SITE_NAME, ADOPTION_STATUS, ONLINE_STATUS, ARTICLE_TYPES } from '../constants/site';

const SPECIES_LABELS = {
  dog: '狗',
  cat: '猫',
  bird: '鸟',
  rabbit: '兔',
  fish: '鱼',
  other: '其他',
};

const ROLE_LABELS = {
  admin: '管理员',
  user: '普通用户',
  visitor: '访客',
};

const MODERATION_ACTION_LABELS = {
  approve: '通过',
  hide: '隐藏',
  delete: '删除',
};

const CONTENT_TYPE_OPTIONS = [
  { value: 'community_post', label: '社区帖子' },
  { value: 'cms_article', label: '资讯文章' },
  { value: 'lost_found_post', label: '报失寻主' },
];

const toList = (data) => (Array.isArray(data) ? data : data?.results ?? []);

const getApiError = (err) => {
  const d = err.response?.data;
  if (typeof d === 'string') return d;
  if (d?.detail) return String(d.detail);
  return err.message || '请求失败';
};

const TABS = [
  { key: 'dashboard', label: '数据概览', icon: 'fa-chart-line' },
  { key: 'users', label: '用户管理', icon: 'fa-users' },
  { key: 'adopt', label: '领养审核', icon: 'fa-clipboard-check' },
  { key: 'pets', label: '宠物管理', icon: 'fa-paw' },
  { key: 'cms', label: '资讯管理', icon: 'fa-newspaper' },
  { key: 'moderation', label: '内容审核', icon: 'fa-shield-alt' },
  { key: 'config', label: '系统配置', icon: 'fa-cog' },
  { key: 'ai-logs', label: 'AI 日志', icon: 'fa-robot' },
];

const KPI_CARDS = [
  { key: 'users', label: '用户', icon: 'fa-users', color: 'primary' },
  { key: 'pets', label: '宠物', icon: 'fa-paw', color: 'success' },
  { key: 'adopt_applications', label: '领养申请', icon: 'fa-heart', color: 'danger' },
  { key: 'rescue_cases', label: '救助案例', icon: 'fa-hand-holding-heart', color: 'warning' },
  { key: 'community_posts', label: '社区帖子', icon: 'fa-comments', color: 'info' },
  { key: 'cms_articles', label: '资讯文章', icon: 'fa-newspaper', color: 'secondary' },
  { key: 'lost_found_posts', label: '寻宠招领', icon: 'fa-search-location', color: 'dark' },
];

const emptyArticleForm = () => ({
  title: '', summary: '', content: '', article_type: 'science', status: 1, is_pinned: false,
});

const AdminDashboard = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState(searchParams.get('tab') || 'dashboard');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [dashboard, setDashboard] = useState(null);
  const [users, setUsers] = useState([]);
  const [applications, setApplications] = useState([]);
  const [pets, setPets] = useState([]);
  const [articles, setArticles] = useState([]);
  const [moderation, setModeration] = useState([]);
  const [configs, setConfigs] = useState([]);
  const [aiLogs, setAiLogs] = useState([]);

  const [auditForm, setAuditForm] = useState({});
  const [modForm, setModForm] = useState({ content_type: 'community_post', content_id: '', action: 'hide', reason: '' });
  const [configEdits, setConfigEdits] = useState({});
  const [articleForm, setArticleForm] = useState(emptyArticleForm());
  const [editingArticleId, setEditingArticleId] = useState(null);
  const [showArticleForm, setShowArticleForm] = useState(false);

  useEffect(() => {
    const tab = searchParams.get('tab');
    if (tab && TABS.some((t) => t.key === tab)) setActiveTab(tab);
  }, [searchParams]);

  const loadTabData = useCallback(async (tab) => {
    setLoading(true);
    setError(null);
    try {
      switch (tab) {
        case 'dashboard': {
          const res = await adminAPI.getDashboard();
          setDashboard(res.data);
          break;
        }
        case 'users': {
          const res = await adminAPI.getUsers();
          setUsers(toList(res.data));
          break;
        }
        case 'adopt': {
          const res = await adoptAPI.getAll();
          setApplications(toList(res.data));
          break;
        }
        case 'pets': {
          const res = await petsAPI.getAll();
          setPets(toList(res.data));
          break;
        }
        case 'cms': {
          const res = await cmsAPI.getArticles();
          setArticles(toList(res.data));
          break;
        }
        case 'moderation': {
          const res = await adminAPI.getModeration();
          setModeration(toList(res.data));
          break;
        }
        case 'config': {
          const res = await adminAPI.getConfig();
          const list = toList(res.data);
          setConfigs(list);
          const edits = {};
          list.forEach((c) => { edits[c.config_key] = c.config_value; });
          setConfigEdits(edits);
          break;
        }
        case 'ai-logs': {
          const res = await adminAPI.getAiLogs();
          setAiLogs(toList(res.data));
          break;
        }
        default:
          break;
      }
    } catch (err) {
      const msg = getApiError(err);
      setError(err.response?.status === 403
        ? `权限不足：${msg}（请确认账号为管理员或运行 fix_admin_roles）`
        : `加载失败：${msg}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTabData(activeTab);
  }, [activeTab, loadTabData]);

  const handleUserUpdate = async (userId, data) => {
    try {
      await adminAPI.updateUser(userId, data);
      loadTabData('users');
    } catch (err) {
      alert('更新失败');
      console.error(err);
    }
  };

  const handleAudit = async (appId) => {
    const form = auditForm[appId] || { online_status: 'approved', audit_opinion: '' };
    try {
      await adoptAPI.audit(appId, form);
      loadTabData('adopt');
    } catch (err) {
      alert('审核失败');
      console.error(err);
    }
  };

  const handleModerationCreate = async (e) => {
    e.preventDefault();
    try {
      await adminAPI.createModeration({
        ...modForm,
        content_id: parseInt(modForm.content_id, 10),
      });
      setModForm({ content_type: '', content_id: '', action: 'hide', reason: '' });
      loadTabData('moderation');
    } catch (err) {
      alert('创建审核记录失败');
      console.error(err);
    }
  };

  const handleConfigSave = async (key) => {
    try {
      await adminAPI.updateConfig(key, { config_value: configEdits[key] });
      alert('配置已保存');
      loadTabData('config');
    } catch (err) {
      alert('保存失败');
      console.error(err);
    }
  };

  const handlePetPatch = async (petId, data) => {
    try {
      await petsAPI.update(petId, data);
      loadTabData('pets');
    } catch (err) {
      alert(getApiError(err));
    }
  };

  const handlePetDelete = async (petId) => {
    if (!window.confirm('确定删除该宠物档案？')) return;
    try {
      await petsAPI.delete(petId);
      loadTabData('pets');
    } catch (err) {
      alert(getApiError(err));
    }
  };

  const openArticleEditor = (article) => {
    if (article) {
      setEditingArticleId(article.id);
      setArticleForm({
        title: article.title || '',
        summary: article.summary || '',
        content: article.content || '',
        article_type: article.article_type || 'science',
        status: article.status ?? 1,
        is_pinned: !!article.is_pinned,
      });
    } else {
      setEditingArticleId(null);
      setArticleForm(emptyArticleForm());
    }
    setShowArticleForm(true);
  };

  const handleArticleSave = async (e) => {
    e.preventDefault();
    try {
      if (editingArticleId) {
        await cmsAPI.updateArticle(editingArticleId, articleForm);
      } else {
        await cmsAPI.createArticle(articleForm);
      }
      setShowArticleForm(false);
      loadTabData('cms');
    } catch (err) {
      alert(getApiError(err));
    }
  };

  const handleArticleStatus = async (id, status) => {
    try {
      await cmsAPI.updateArticle(id, { status });
      loadTabData('cms');
    } catch (err) {
      alert(getApiError(err));
    }
  };

  const switchTab = (key) => {
    setActiveTab(key);
    setSearchParams({ tab: key });
  };

  const renderDashboard = () => (
    <div>
      <div className="row g-3 mb-4">
        {KPI_CARDS.map((card) => (
          <div key={card.key} className="col-md-4 col-lg-3">
            <div className={`card border-${card.color} h-100`}>
              <div className="card-body text-center">
                <i className={`fas ${card.icon} fa-2x text-${card.color} mb-2`}></i>
                <h3 className="mb-0">{dashboard?.[card.key] ?? '-'}</h3>
                <small className="text-muted">{card.label}</small>
              </div>
            </div>
          </div>
        ))}
      </div>
      {dashboard?.adopt_by_status?.length > 0 && (
        <div className="card">
          <div className="card-header">领养申请状态分布</div>
          <div className="card-body">
            <div className="d-flex flex-wrap gap-2">
              {dashboard.adopt_by_status.map((item) => (
                <span key={item.online_status} className="badge bg-secondary fs-6">
                  {ONLINE_STATUS[item.online_status] || item.online_status}：{item.count}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const renderUsers = () => (
    <div className="table-responsive">
      <table className="table table-hover">
        <thead>
          <tr>
            <th>用户名</th>
            <th>邮箱</th>
            <th>角色</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td>{ROLE_LABELS[user.profile?.role] || user.profile?.role || '-'}</td>
              <td>{user.profile?.status === 1 ? '正常' : '禁用'}</td>
              <td>
                <div className="btn-group btn-group-sm">
                  <button type="button" className="btn btn-outline-success" onClick={() => handleUserUpdate(user.id, { status: 1 })}>启用</button>
                  <button type="button" className="btn btn-outline-danger" onClick={() => handleUserUpdate(user.id, { status: 0 })}>禁用</button>
                  <button type="button" className="btn btn-outline-primary" onClick={() => handleUserUpdate(user.id, { role: 'admin' })}>设为管理员</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  const renderAdoptAudit = () => (
    <div className="table-responsive">
      <table className="table table-hover">
        <thead>
          <tr>
            <th>申请人</th>
            <th>宠物</th>
            <th>留言</th>
            <th>状态</th>
            <th>审核</th>
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
                      <option value="approved">通过</option>
                      <option value="rejected">拒绝</option>
                      <option value="need_material">需补材料</option>
                    </select>
                    <input
                      type="text"
                      className="form-control form-control-sm"
                      placeholder="审核意见"
                      value={auditForm[app.id]?.audit_opinion || ''}
                      onChange={(e) => setAuditForm({ ...auditForm, [app.id]: { ...auditForm[app.id], audit_opinion: e.target.value } })}
                    />
                    <button type="button" className="btn btn-success btn-sm" onClick={() => handleAudit(app.id)}>提交审核</button>
                  </div>
                ) : (
                  <small className="text-muted">{app.audit_opinion || '已审核'}</small>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  const renderPets = () => (
    <div>
      <div className="mb-3">
        <Link to="/add-pet" className="btn btn-success btn-sm">新建宠物档案</Link>
      </div>
      <div className="row">
        {pets.map((pet) => (
          <div key={pet.id} className="col-md-4 mb-3">
            <div className="card h-100">
              <div className="card-body">
                <h6>{pet.name || SPECIES_LABELS[pet.species] || pet.species}</h6>
                <small className="text-muted d-block mb-2">
                  {SPECIES_LABELS[pet.species] || pet.species} · {ADOPTION_STATUS[pet.adoption_status] || pet.adoption_status}
                  <br />公开：{pet.is_public ? '是' : '否'}
                </small>
                <div className="d-flex flex-wrap gap-1">
                  <Link to={`/pets/${pet.id}`} className="btn btn-outline-secondary btn-sm">前台</Link>
                  <button type="button" className="btn btn-outline-primary btn-sm" onClick={() => handlePetPatch(pet.id, { is_public: !pet.is_public })}>
                    {pet.is_public ? '隐藏' : '公开'}
                  </button>
                  <button type="button" className="btn btn-outline-warning btn-sm" onClick={() => handlePetPatch(pet.id, { adoption_status: 'available' })}>可领养</button>
                  <button type="button" className="btn btn-outline-danger btn-sm" onClick={() => handlePetDelete(pet.id)}>删除</button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderCms = () => (
    <div>
      <button type="button" className="btn btn-success btn-sm mb-3" onClick={() => openArticleEditor(null)}>新建文章</button>
      {showArticleForm && (
        <form className="card mb-3" onSubmit={handleArticleSave}>
          <div className="card-body row g-2">
            <div className="col-md-6"><input className="form-control" placeholder="标题" value={articleForm.title} onChange={(e) => setArticleForm({ ...articleForm, title: e.target.value })} required /></div>
            <div className="col-md-3">
              <select className="form-select" value={articleForm.article_type} onChange={(e) => setArticleForm({ ...articleForm, article_type: e.target.value })}>
                {Object.entries(ARTICLE_TYPES).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </div>
            <div className="col-md-3">
              <select className="form-select" value={articleForm.status} onChange={(e) => setArticleForm({ ...articleForm, status: Number(e.target.value) })}>
                <option value={0}>草稿</option>
                <option value={1}>已发布</option>
                <option value={2}>已下线</option>
              </select>
            </div>
            <div className="col-12"><input className="form-control" placeholder="摘要" value={articleForm.summary} onChange={(e) => setArticleForm({ ...articleForm, summary: e.target.value })} /></div>
            <div className="col-12"><textarea className="form-control" rows={4} placeholder="正文" value={articleForm.content} onChange={(e) => setArticleForm({ ...articleForm, content: e.target.value })} required /></div>
            <div className="col-12">
              <button type="submit" className="btn btn-primary btn-sm me-2">保存</button>
              <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setShowArticleForm(false)}>取消</button>
            </div>
          </div>
        </form>
      )}
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr><th>标题</th><th>类型</th><th>状态</th><th>操作</th></tr>
          </thead>
          <tbody>
            {articles.map((article) => (
              <tr key={article.id}>
                <td><Link to={`/cms/${article.id}`}>{article.title}</Link></td>
                <td>{ARTICLE_TYPES[article.article_type] || article.article_type}</td>
                <td>{article.status === 1 ? '已发布' : article.status === 0 ? '草稿' : '已下线'}</td>
                <td>
                  <div className="btn-group btn-group-sm">
                    <button type="button" className="btn btn-outline-primary" onClick={() => openArticleEditor(article)}>编辑</button>
                    {article.status !== 1 && <button type="button" className="btn btn-outline-success" onClick={() => handleArticleStatus(article.id, 1)}>发布</button>}
                    {article.status === 1 && <button type="button" className="btn btn-outline-warning" onClick={() => handleArticleStatus(article.id, 2)}>下线</button>}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderModeration = () => (
    <div>
      <form onSubmit={handleModerationCreate} className="card mb-4">
        <div className="card-header">新建审核操作</div>
        <div className="card-body row g-2">
          <div className="col-md-3">
            <select className="form-select" value={modForm.content_type} onChange={(e) => setModForm({ ...modForm, content_type: e.target.value })} required>
              {CONTENT_TYPE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </div>
          <div className="col-md-2">
            <input type="number" className="form-control" placeholder="内容 ID" value={modForm.content_id} onChange={(e) => setModForm({ ...modForm, content_id: e.target.value })} required />
          </div>
          <div className="col-md-2">
            <select className="form-select" value={modForm.action} onChange={(e) => setModForm({ ...modForm, action: e.target.value })}>
              {Object.entries(MODERATION_ACTION_LABELS).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </div>
          <div className="col-md-3">
            <input type="text" className="form-control" placeholder="原因" value={modForm.reason} onChange={(e) => setModForm({ ...modForm, reason: e.target.value })} />
          </div>
          <div className="col-md-2">
            <button type="submit" className="btn btn-success w-100">提交</button>
          </div>
        </div>
      </form>
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th>类型</th>
              <th>ID</th>
              <th>操作</th>
              <th>原因</th>
              <th>操作人</th>
              <th>时间</th>
            </tr>
          </thead>
          <tbody>
            {moderation.map((item) => (
              <tr key={item.id}>
                <td>{item.content_type}</td>
                <td>{item.content_id}</td>
                <td><span className="badge bg-warning text-dark">{MODERATION_ACTION_LABELS[item.action] || item.action}</span></td>
                <td>{item.reason}</td>
                <td>{item.operator?.username}</td>
                <td>{new Date(item.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderConfig = () => (
    <div className="list-group">
      {configs.map((cfg) => (
        <div key={cfg.config_key} className="list-group-item">
          <div className="d-flex justify-content-between align-items-start mb-2">
            <div>
              <strong>{cfg.config_key}</strong>
              {cfg.description && <small className="text-muted d-block">{cfg.description}</small>}
            </div>
          </div>
          <div className="input-group">
            <input
              type="text"
              className="form-control"
              value={configEdits[cfg.config_key] ?? ''}
              onChange={(e) => setConfigEdits({ ...configEdits, [cfg.config_key]: e.target.value })}
            />
            <button type="button" className="btn btn-success" onClick={() => handleConfigSave(cfg.config_key)}>保存</button>
          </div>
        </div>
      ))}
    </div>
  );

  const renderAiLogs = () => (
    <div className="table-responsive">
      <table className="table table-hover table-sm">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户</th>
            <th>功能</th>
            <th>成功</th>
            <th>请求</th>
            <th>时间</th>
          </tr>
        </thead>
        <tbody>
          {aiLogs.map((log) => (
            <tr key={log.id}>
              <td>{log.id}</td>
              <td>{log.user?.username || log.user}</td>
              <td>{log.feature_type}</td>
              <td>{log.success ? '是' : '否'}</td>
              <td style={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>{log.request_meta}</td>
              <td>{new Date(log.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'dashboard': return renderDashboard();
      case 'users': return renderUsers();
      case 'adopt': return renderAdoptAudit();
      case 'pets': return renderPets();
      case 'cms': return renderCms();
      case 'moderation': return renderModeration();
      case 'config': return renderConfig();
      case 'ai-logs': return renderAiLogs();
      default: return null;
    }
  };

  return (
    <div className="py-3">
      <h2 className="mb-4"><i className="fas fa-cog me-2"></i>{SITE_NAME} 管理后台</h2>

      <div className="row">
        <div className="col-md-3 col-lg-2">
          <div className="list-group mb-4">
            {TABS.map((tab) => (
              <button
                key={tab.key}
                type="button"
                className={`list-group-item list-group-item-action ${activeTab === tab.key ? 'active' : ''}`}
                onClick={() => switchTab(tab.key)}
              >
                <i className={`fas ${tab.icon} me-2`}></i>{tab.label}
              </button>
            ))}
          </div>
        </div>
        <div className="col-md-9 col-lg-10">
          {error && <div className="alert alert-danger">{error}</div>}
          {loading ? (
            <div className="text-center py-5">
              <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">加载中...</span>
              </div>
            </div>
          ) : (
            <div className="card shadow-sm">
              <div className="card-header">
                <h5 className="mb-0">{TABS.find((t) => t.key === activeTab)?.label}</h5>
              </div>
              <div className="card-body">{renderTabContent()}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
