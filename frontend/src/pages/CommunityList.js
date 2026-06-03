import React, { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { adminAPI, communityAPI } from '../api/api';
import AdminManageBar from '../components/AdminManageBar';
import { POST_CATEGORIES } from '../constants/site';

const CATEGORY_TABS = [
  { key: '', label: '全部' },
  ...Object.entries(POST_CATEGORIES).map(([key, label]) => ({ key, label })),
];

const ORDER_OPTIONS = [
  { key: 'latest', label: '最新发布' },
  { key: 'likes', label: '最多点赞' },
];

const CommunityList = () => {
  const [posts, setPosts] = useState([]);
  const [category, setCategory] = useState('');
  const [searchInput, setSearchInput] = useState('');
  const [searchQ, setSearchQ] = useState('');
  const [ordering, setOrdering] = useState('latest');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [likingId, setLikingId] = useState(null);

  useEffect(() => {
    const timer = setTimeout(() => setSearchQ(searchInput.trim()), 300);
    return () => clearTimeout(timer);
  }, [searchInput]);

  const fetchPosts = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const params = { ordering };
      if (category) params.category = category;
      if (searchQ) params.q = searchQ;
      const response = await communityAPI.getPosts(params);
      setPosts(Array.isArray(response.data) ? response.data : response.data?.results ?? []);
    } catch (err) {
      setError('加载帖子失败，请稍后重试。');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [category, searchQ, ordering]);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

  const handleAdminDelete = async (postId) => {
    if (!window.confirm('确定删除该帖子？')) return;
    try {
      await communityAPI.deletePost(postId);
      fetchPosts();
    } catch (err) {
      alert('删除失败');
    }
  };

  const handleBanUser = async (userId) => {
    if (!window.confirm('确定封禁该用户？')) return;
    try {
      await adminAPI.updateUser(userId, { status: 1 });
      alert('已封禁');
    } catch (err) {
      alert('操作失败');
    }
  };

  const handleLike = async (post) => {
    if (!localStorage.getItem('token')) {
      alert('请先登录后再点赞');
      return;
    }
    setLikingId(post.id);
    try {
      if (post.is_liked) {
        await communityAPI.unlikePost(post.id);
      } else {
        await communityAPI.likePost(post.id);
      }
      setPosts((prev) =>
        prev.map((p) =>
          p.id === post.id
            ? {
                ...p,
                is_liked: !p.is_liked,
                like_count: p.is_liked ? Math.max(0, p.like_count - 1) : p.like_count + 1,
              }
            : p
        )
      );
    } catch (err) {
      console.error(err);
      alert('操作失败');
    } finally {
      setLikingId(null);
    }
  };

  return (
    <div className="py-3">
      <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
        <h2><i className="fas fa-comments me-2 text-success"></i>社区交流</h2>
        <Link to="/community/publish" className="btn btn-success">
          <i className="fas fa-pen me-1"></i>发帖
        </Link>
      </div>

      <div className="row g-2 mb-3">
        <div className="col-md-8">
          <div className="input-group">
            <span className="input-group-text"><i className="fas fa-search" /></span>
            <input
              type="search"
              className="form-control"
              placeholder="搜索标题或正文..."
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
            />
          </div>
        </div>
        <div className="col-md-4">
          <select
            className="form-select"
            value={ordering}
            onChange={(e) => setOrdering(e.target.value)}
          >
            {ORDER_OPTIONS.map((opt) => (
              <option key={opt.key} value={opt.key}>{opt.label}</option>
            ))}
          </select>
        </div>
      </div>

      <ul className="nav nav-pills mb-4 flex-wrap gap-1">
        {CATEGORY_TABS.map((tab) => (
          <li className="nav-item" key={tab.key || 'all'}>
            <button
              type="button"
              className={`nav-link ${category === tab.key ? 'active' : ''}`}
              onClick={() => setCategory(tab.key)}
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
        <div className="list-group">
          {posts.length === 0 ? (
            <div className="text-center text-muted py-5">暂无帖子</div>
          ) : (
            posts.map((post) => (
              <div key={post.id} className="list-group-item list-group-item-action mb-2 rounded shadow-sm">
                <AdminManageBar
                  userId={post.author?.id}
                  onHide={() => handleAdminDelete(post.id)}
                  onDelete={() => handleAdminDelete(post.id)}
                  onBanUser={() => handleBanUser(post.author.id)}
                />
                <div className="d-flex w-100 justify-content-between align-items-start">
                  <div className="flex-grow-1 text-start">
                    <div className="mb-1">
                      <span className="badge bg-success me-2">
                        {POST_CATEGORIES[post.category] || post.category}
                      </span>
                      {post.author && (
                        <Link to={`/users/${post.author.id}`} className="text-muted small">{post.author.username}</Link>
                      )}
                    </div>
                    <Link to={`/community/${post.id}`} className="text-decoration-none text-dark d-block text-start">
                      <h5 className="mb-1">{post.title}</h5>
                    </Link>
                    <p className="mb-2 text-muted small text-start">{post.content?.slice(0, 120)}</p>
                    <small className="text-muted">
                      {new Date(post.created_at).toLocaleString()} · {post.comment_count} 评论
                    </small>
                  </div>
                  <button
                    type="button"
                    className={`btn btn-sm ms-3 flex-shrink-0 ${post.is_liked ? 'btn-danger' : 'btn-outline-danger'}`}
                    onClick={() => handleLike(post)}
                    disabled={likingId === post.id}
                  >
                    <i className="fas fa-heart me-1"></i>{post.like_count}
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default CommunityList;
