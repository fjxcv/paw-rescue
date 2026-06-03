import React, { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { adminAPI, lostFoundAPI } from '../api/api';
import AdminManageBar from '../components/AdminManageBar';
import { LOST_FOUND_STATUS, LOST_FOUND_TYPE } from '../constants/site';

const POST_TYPE_TABS = [
  { key: '', label: '全部类型' },
  ...Object.entries(LOST_FOUND_TYPE).map(([key, label]) => ({ key, label })),
];

const STATUS_TABS = [
  { key: '', label: '全部状态' },
  ...Object.entries(LOST_FOUND_STATUS).map(([key, label]) => ({ key, label })),
];

const LostFoundList = () => {
  const [posts, setPosts] = useState([]);
  const [postType, setPostType] = useState('');
  const [status, setStatus] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [searchQ, setSearchQ] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const timer = setTimeout(() => setSearchQ(searchInput.trim()), 300);
    return () => clearTimeout(timer);
  }, [searchInput]);

  const fetchPosts = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const params = {};
      if (postType) params.post_type = postType;
      if (status) params.status = status;
      if (searchQ) params.q = searchQ;
      const response = await lostFoundAPI.getAll(params);
      setPosts(Array.isArray(response.data) ? response.data : response.data?.results ?? []);
    } catch (err) {
      setError('加载信息失败，请稍后重试。');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [postType, status, searchQ]);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  return (
    <div className="py-3">
      <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
        <h2><i className="fas fa-search-location me-2 text-success"></i>报失寻主</h2>
        <Link to="/lost-found/publish" className="btn btn-success">
          <i className="fas fa-plus me-1"></i>发布信息
        </Link>
      </div>

      <div className="mb-3">
        <div className="input-group">
          <span className="input-group-text"><i className="fas fa-search" /></span>
          <input
            type="search"
            className="form-control"
            placeholder="搜索物种、特征、地址..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
        </div>
      </div>

      <ul className="nav nav-pills mb-2 flex-wrap gap-1">
        {POST_TYPE_TABS.map((tab) => (
          <li className="nav-item" key={`type-${tab.key || 'all'}`}>
            <button
              type="button"
              className={`nav-link ${postType === tab.key ? 'active' : ''}`}
              onClick={() => setPostType(tab.key)}
            >
              {tab.label}
            </button>
          </li>
        ))}
      </ul>

      <ul className="nav nav-pills mb-4 flex-wrap gap-1">
        {STATUS_TABS.map((tab) => (
          <li className="nav-item" key={`status-${tab.key || 'all'}`}>
            <button
              type="button"
              className={`nav-link ${status === tab.key ? 'active' : ''}`}
              onClick={() => setStatus(tab.key)}
            >
              {tab.label}
            </button>
          </li>
        ))}
      </ul>

      {loading && (
        <div className="text-center py-5">
          <div className="spinner-border text-success" role="status">
            <span className="visually-hidden">加载中...</span>
          </div>
        </div>
      )}

      {error && <div className="alert alert-danger">{error}</div>}

      {!loading && !error && (
        <div className="row">
          {posts.length === 0 ? (
            <div className="col-12 text-center text-muted py-5">暂无信息</div>
          ) : (
            posts.map((post) => (
              <div key={post.id} className="col-md-6 col-lg-4 mb-4">
                <div className="card h-100 shadow-sm">
                  {post.photo_urls?.[0] && (
                    <img
                      src={post.photo_urls[0]}
                      className="card-img-top"
                      alt={post.pet_species}
                      style={{ height: '180px', objectFit: 'cover' }}
                    />
                  )}
                  <div className="card-body text-start">
                    <AdminManageBar
                      userId={post.publisher?.id}
                      onHide={async () => {
                        await lostFoundAPI.update(post.id, { status: 'cancelled' });
                        fetchPosts();
                      }}
                      onBanUser={post.publisher?.id ? async () => {
                        await adminAPI.updateUser(post.publisher.id, { status: 1 });
                        alert('已封禁');
                      } : undefined}
                    />
                    <div className="mb-2">
                      <span className={`badge ${post.post_type === 'lost' ? 'bg-danger' : 'bg-info'}`}>
                        {LOST_FOUND_TYPE[post.post_type] || post.post_type}
                      </span>
                      <span className="badge bg-secondary ms-1">
                        {LOST_FOUND_STATUS[post.status] || post.status}
                      </span>
                    </div>
                    <h5 className="card-title text-start">{post.pet_species}</h5>
                    <p className="card-text text-muted small text-start">{post.features?.slice(0, 80)}</p>
                    {post.address_text && (
                      <p className="small mb-2 text-start"><i className="fas fa-map-marker-alt me-1"></i>{post.address_text}</p>
                    )}
                    {Number(post.reward_amount) > 0 && (
                      <p className="small text-warning mb-2">悬赏 {post.reward_amount} 元</p>
                    )}
                    <Link to={`/lost-found/${post.id}`} className="btn btn-outline-success btn-sm w-100">
                      查看详情
                    </Link>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default LostFoundList;
