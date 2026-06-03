import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { communityAPI } from '../api/api';
import { POST_CATEGORIES } from '../constants/site';

const CATEGORY_OPTIONS = Object.entries(POST_CATEGORIES).map(([value, label]) => ({ value, label }));

const CommunityPostEdit = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({ category: 'general', title: '', content: '' });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    (async () => {
      try {
        const res = await communityAPI.getPost(id);
        setForm({
          category: res.data.category,
          title: res.data.title,
          content: res.data.content,
        });
      } catch (err) {
        setError('无法加载帖子');
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      await communityAPI.updatePost(id, form);
      navigate(`/community/${id}`);
    } catch (err) {
      setError(err.response?.data?.detail || '保存失败，请重试。');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-success" />
      </div>
    );
  }

  return (
    <div className="py-3">
      <nav aria-label="breadcrumb" className="mb-3">
        <ol className="breadcrumb">
          <li className="breadcrumb-item"><Link to="/community">社区交流</Link></li>
          <li className="breadcrumb-item"><Link to={`/community/${id}`}>帖子</Link></li>
          <li className="breadcrumb-item active">编辑</li>
        </ol>
      </nav>

      <h2 className="mb-4"><i className="fas fa-edit me-2 text-success" />编辑帖子</h2>

      {error && <div className="alert alert-danger">{error}</div>}

      <form onSubmit={handleSubmit} className="card shadow-sm">
        <div className="card-body">
          <div className="mb-3">
            <label className="form-label">分类</label>
            <select name="category" className="form-select" value={form.category} onChange={handleChange} required>
              {CATEGORY_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
          <div className="mb-3">
            <label className="form-label">标题</label>
            <input type="text" name="title" className="form-control" value={form.title} onChange={handleChange} required maxLength={200} />
          </div>
          <div className="mb-3">
            <label className="form-label">内容</label>
            <textarea name="content" className="form-control" rows={8} value={form.content} onChange={handleChange} required />
          </div>
        </div>
        <div className="card-footer d-flex gap-2">
          <button type="submit" className="btn btn-success" disabled={submitting}>
            {submitting ? '保存中...' : '保存'}
          </button>
          <Link to={`/community/${id}`} className="btn btn-outline-secondary">取消</Link>
        </div>
      </form>
    </div>
  );
};

export default CommunityPostEdit;
