# -*- coding: utf-8 -*-
from pathlib import Path

content = r'''import React, { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { cmsAPI } from '../api/api';
import { ARTICLE_TYPES } from '../constants/site';

const CmsDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const fetchedRef = useRef(false);

  useEffect(() => {
    if (fetchedRef.current) return;
    fetchedRef.current = true;
    const fetchArticle = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await cmsAPI.getArticle(id);
        setArticle(response.data);
      } catch (err) {
        setError('\u6587\u7ae0\u4e0d\u5b58\u5728\u6216\u52a0\u8f7d\u5931\u8d25\u3002');
        console.error('Error fetching article:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchArticle();
  }, [id]);

  const requireAuth = () => {
    if (!localStorage.getItem('token')) {
      alert('\u8bf7\u5148\u767b\u5f55');
      navigate('/login');
      return false;
    }
    return true;
  };

  const handleFavorite = async () => {
    if (!requireAuth()) return;
    setActionLoading(true);
    try {
      if (article.is_favorited) {
        await cmsAPI.unfavoriteArticle(id);
        setArticle((a) => ({ ...a, is_favorited: false }));
      } else {
        await cmsAPI.favoriteArticle(id);
        setArticle((a) => ({ ...a, is_favorited: true }));
      }
    } catch (err) {
      console.error(err);
      alert('\u6536\u85cf\u64cd\u4f5c\u5931\u8d25\uff0c\u8bf7\u91cd\u8bd5\u3002');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-success" role="status">
          <span className="visually-hidden">\u52a0\u8f7d\u4e2d...</span>
        </div>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="text-center">
        <div className="alert alert-danger">{error || '\u6587\u7ae0\u672a\u627e\u5230'}</div>
        <Link to="/cms" className="btn btn-outline-secondary">\u8fd4\u56de\u5217\u8868</Link>
      </div>
    );
  }

  return (
    <div className="py-3">
      <nav aria-label="breadcrumb" className="mb-3">
        <ol className="breadcrumb">
          <li className="breadcrumb-item"><Link to="/">\u9996\u9875</Link></li>
          <li className="breadcrumb-item"><Link to="/cms">\u8d44\u8baf\u4e2d\u5fc3</Link></li>
          <li className="breadcrumb-item active">{article.title}</li>
        </ol>
      </nav>

      <article className="card shadow-sm">
        {article.cover_url && (
          <img src={article.cover_url} className="card-img-top" alt={article.title} style={{ maxHeight: '400px', objectFit: 'cover' }} />
        )}
        <div className="card-body">
          <div className="mb-3">
            <span className="badge bg-success me-2">
              {ARTICLE_TYPES[article.article_type] || article.article_type}
            </span>
            {article.is_pinned && <span className="badge bg-warning text-dark">\u7f6e\u9876</span>}
          </div>
          <h1 className="card-title mb-3">{article.title}</h1>
          <div className="text-muted small mb-4">
            {article.author && <span className="me-3"><i className="fas fa-user me-1"></i>{article.author.username}</span>}
            <span className="me-3"><i className="fas fa-eye me-1"></i>{article.view_count || 0} \u6b21\u9605\u8bfb</span>
            {article.published_at && (
              <span><i className="fas fa-calendar me-1"></i>{new Date(article.published_at).toLocaleDateString()}</span>
            )}
          </div>
          {article.summary && <p className="lead text-muted">{article.summary}</p>}
          <div className="article-content markdown-preview" style={{ lineHeight: 1.8 }}>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{article.content || ''}</ReactMarkdown>
          </div>
        </div>
      </article>

      <div className="mt-4 d-flex flex-wrap justify-content-center gap-2">
        <button
          type="button"
          className={`btn ${article.is_favorited ? 'btn-warning' : 'btn-outline-warning'}`}
          onClick={handleFavorite}
          disabled={actionLoading}
        >
          <i className="fas fa-star me-1"></i>
          {article.is_favorited ? '\u5df2\u6536\u85cf' : '\u6536\u85cf'}
        </button>
        <Link to="/cms" className="btn btn-outline-secondary">
          <i className="fas fa-arrow-left me-1"></i>\u8fd4\u56de\u5217\u8868
        </Link>
      </div>
    </div>
  );
};

export default CmsDetail;
'''

path = Path(__file__).resolve().parent.parent / 'frontend/src/pages/CmsDetail.js'
path.write_text(content.encode('utf-8').decode('unicode_escape'), encoding='utf-8', newline='\n')
print('CmsDetail patched')
