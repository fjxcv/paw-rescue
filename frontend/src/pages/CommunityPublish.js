import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { communityAPI } from '../api/api';
import { POST_CATEGORIES } from '../constants/site';

const CATEGORY_OPTIONS = Object.entries(POST_CATEGORIES).map(([value, label]) => ({ value, label }));

const CommunityPublish = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({ category: 'general', title: '', content: '' });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      const res = await communityAPI.createPost(form);
      navigate(`/community/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || '发帖失败，请重试。');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="py-3">
      <nav aria-label="breadcrumb" className="mb-3">
        <ol className="breadcrumb">
          <li className="breadcrumb-item"><Link to="/community">社区交流</Link></li>
          <li className="breadcrumb-item active">发帖</li>
        </ol>
      </nav>

      <h2 className="mb-4"><i className="fas fa-pen me-2 text-success"></i>发布帖子</h2>

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
            <input type="text" name="title" className="form-control" value={form.title} onChange={handleChange} required maxLength={200} placeholder="请输入帖子标题" />
          </div>
          <div className="mb-3">
            <label className="form-label">内容</label>
            <textarea name="content" className="form-control" rows={8} value={form.content} onChange={handleChange} required placeholder="请输入帖子内容" />
          </div>
        </div>
        <div className="card-footer d-flex gap-2">
          <button type="submit" className="btn btn-success" disabled={submitting}>
            {submitting ? '发布中...' : '发布'}
          </button>
          <Link to="/community" className="btn btn-outline-secondary">取消</Link>
        </div>
      </form>
    </div>
  );
};

export default CommunityPublish;
