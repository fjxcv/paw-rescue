import React, { useEffect, useRef, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { authAPI, lostFoundAPI } from '../api/api';
import { LOST_FOUND_STATUS, LOST_FOUND_TYPE } from '../constants/site';

const LostFoundDetail = () => {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentUserId, setCurrentUserId] = useState(null);
  const detailMapRef = useRef(null);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        setLoading(true);
        setError(null);
        const [postRes, profileRes] = await Promise.all([
          lostFoundAPI.getById(id),
          authAPI.getProfile().catch(() => ({ data: null })),
        ]);
        setPost(postRes.data);
        setCurrentUserId(profileRes.data?.id || null);
      } catch (err) {
        setError('加载详情失败，请稍后重试。');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchPost();
  }, [id]);

  const handleMarkFound = async () => {
    try {
      await lostFoundAPI.update(id, { status: 'found' });
      setPost((prev) => ({ ...prev, status: 'found' }));
    } catch (err) {
      alert('操作失败');
    }
  };

  const handleCancel = async () => {
    if (!window.confirm('确定要撤销这条发布吗？')) return;
    try {
      await lostFoundAPI.update(id, { status: 'cancelled' });
      setPost((prev) => ({ ...prev, status: 'cancelled' }));
    } catch (err) {
      alert('操作失败');
    }
  };

  const canManage = currentUserId && post?.publisher?.id === currentUserId;

  // 详情页地图
  useEffect(() => {
    const mapContainer = detailMapRef.current;
    if (!mapContainer || post?.latitude == null || post?.longitude == null) return;

    const lat = parseFloat(post.latitude);
    const lng = parseFloat(post.longitude);
    if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;

    let mapInstance = null;
    let scriptElement = null;
    let linkElement = null;

    const initMap = () => {
      if (!mapContainer || mapContainer._leaflet_map) return;
      try {
        const L = window.L;
        mapInstance = L.map(mapContainer).setView([lat, lng], 15);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: '&copy; OpenStreetMap',
        }).addTo(mapInstance);
        L.marker([lat, lng]).addTo(mapInstance);
      } catch (e) {
        console.error('Map init error:', e);
      }
    };

    if (window.L) {
      initMap();
    } else {
      // 动态加载 Leaflet
      linkElement = document.createElement('link');
      linkElement.rel = 'stylesheet';
      linkElement.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      document.head.appendChild(linkElement);

      scriptElement = document.createElement('script');
      scriptElement.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      scriptElement.onload = initMap;
      scriptElement.onerror = () => console.error('Leaflet script load failed');
      document.body.appendChild(scriptElement);
    }

    return () => {
      if (mapInstance) {
        mapInstance.remove();
        mapInstance = null;
      }
    };
  }, [post]);

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-success" role="status">
          <span className="visually-hidden">加载中...</span>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div>
        <div className="alert alert-danger">{error || '未找到该信息'}</div>
        <Link to="/lost-found" className="btn btn-outline-secondary">返回列表</Link>
      </div>
    );
  }

  return (
    <div className="py-3">
      <nav aria-label="breadcrumb" className="mb-3">
        <ol className="breadcrumb">
          <li className="breadcrumb-item"><Link to="/lost-found">报失寻主</Link></li>
          <li className="breadcrumb-item active">{post.pet_species}</li>
        </ol>
      </nav>

      <div className="card shadow-sm">
        <div className="card-body">
          <div className="mb-3">
            <span className={`badge ${post.post_type === 'lost' ? 'bg-danger' : 'bg-info'} me-2`}>
              {LOST_FOUND_TYPE[post.post_type] || post.post_type}
            </span>
            <span className={`badge ${post.status === 'searching' ? 'bg-warning text-dark' : post.status === 'found' ? 'bg-success' : 'bg-secondary'}`}>
              {LOST_FOUND_STATUS[post.status] || post.status}
            </span>
          </div>

          <h2 className="mb-3">{post.pet_species}</h2>

          {post.photo_urls?.length > 0 && (
            <div className="d-flex flex-wrap justify-content-center align-items-center gap-3 mb-4">
              {post.photo_urls.map((url, idx) => (
                <img
                  key={idx}
                  src={url}
                  alt={post.pet_species}
                  className="img-fluid rounded shadow-sm"
                  style={{ maxHeight: '360px', maxWidth: 'min(100%, 480px)', objectFit: 'contain' }}
                />
              ))}
            </div>
          )}

          <h5>体征特征</h5>
          <p style={{ whiteSpace: 'pre-wrap' }}>{post.features}</p>

          <hr />

          <div className="row">
            <div className="col-md-6 mb-3">
              <h6><i className="fas fa-map-marker-alt me-2 text-success"></i>位置</h6>
              <p className="mb-1">{post.address_text || '未填写地址'}</p>
              {post.latitude != null && post.longitude != null && (
                <div
                  ref={detailMapRef}
                  style={{ width: '100%', height: 200, borderRadius: 8, border: '1px solid #ddd', marginTop: 8 }}
                />
              )}
            </div>
            {Number(post.reward_amount) > 0 && (
              <div className="col-md-6 mb-3">
                <h6><i className="fas fa-gift me-2 text-warning"></i>悬赏</h6>
                <p className="text-warning fw-bold">{post.reward_amount} 元</p>
              </div>
            )}
            {post.contact_phone && (
              <div className="col-md-6 mb-3">
                <h6><i className="fas fa-phone me-2"></i>联系电话</h6>
                <p>{post.contact_phone_display || post.contact_phone}</p>
              </div>
            )}
            {post.publisher && (
              <div className="col-md-6 mb-3">
                <h6><i className="fas fa-user me-2"></i>发布者</h6>
                <p>{post.publisher.username}</p>
              </div>
            )}
          </div>

          <small className="text-muted">
            发布时间：{new Date(post.created_at).toLocaleString()}
          </small>
        </div>
      </div>

      <div className="mt-4 d-flex gap-2 flex-wrap">
        <Link to="/lost-found" className="btn btn-outline-secondary">
          <i className="fas fa-arrow-left me-1"></i>返回列表
        </Link>
        {canManage && post.status === 'searching' && (
          <>
            <button className="btn btn-outline-primary" onClick={handleMarkFound}>
              <i className="fas fa-check me-1"></i>标记已找回
            </button>
            <button className="btn btn-outline-danger" onClick={handleCancel}>
              <i className="fas fa-times me-1"></i>撤销发布
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default LostFoundDetail;
