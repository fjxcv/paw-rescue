import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { aiAPI, lostFoundAPI, uploadAPI } from '../api/api';
import { LOST_FOUND_TYPE } from '../constants/site';
import { formatApiError, roundCoordinate } from '../utils/apiError';

const LostFoundPublish = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    post_type: 'lost',
    pet_species: '',
    features: '',
    latitude: '',
    longitude: '',
    address_text: '',
    reward_amount: '0',
    contact_phone: '',
  });
  const [photoUrls, setPhotoUrls] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [locating, setLocating] = useState(false);
  const [locationHint, setLocationHint] = useState('');
  const [error, setError] = useState('');

  const hasCoordinates = () => {
    const lat = parseFloat(form.latitude);
    const lng = parseFloat(form.longitude);
    return Number.isFinite(lat) && Number.isFinite(lng);
  };

  const handleUseCurrentLocation = () => {
    if (!navigator.geolocation) {
      setError('当前浏览器不支持定位，请换用手机浏览器或 Chrome/Edge。');
      return;
    }
    setError('');
    setLocating(true);
    setLocationHint('');
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setForm((f) => ({
          ...f,
          latitude: String(roundCoordinate(pos.coords.latitude)),
          longitude: String(roundCoordinate(pos.coords.longitude)),
        }));
        const meters = Math.round(pos.coords.accuracy);
        setLocationHint(`已记录当前位置（定位精度约 ${meters} 米，便于他人查找）`);
        setLocating(false);
      },
      (geoErr) => {
        setLocating(false);
        const hints = {
          1: '您拒绝了位置权限，请在浏览器设置中允许定位后重试。',
          2: '暂时无法获取位置，请稍后重试或检查系统定位是否开启。',
          3: '定位超时，请到开阔处重试。',
        };
        setError(hints[geoErr.code] || '获取位置失败，请检查浏览器定位权限。');
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 120000 },
    );
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handlePhotoUpload = async (e) => {
    const files = Array.from(e.target.files);
    if (!files.length) return;
    setUploading(true);
    setError('');
    try {
      const uploaded = [];
      for (const file of files) {
        const res = await uploadAPI.upload(file, 'lost-found');
        uploaded.push(res.data.url);
      }
      setPhotoUrls((prev) => [...prev, ...uploaded]);
    } catch (err) {
      setError('图片上传失败，请重试。');
      console.error(err);
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  };

  const removePhoto = (index) => {
    setPhotoUrls((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const address = form.address_text.trim();
    if (!address) {
      setError('请填写事发地点或附近地标。');
      return;
    }
    setSubmitting(true);
    setError('');
    try {
      const lat = roundCoordinate(form.latitude);
      const lng = roundCoordinate(form.longitude);
      const payload = {
        post_type: form.post_type,
        pet_species: form.pet_species,
        features: form.features,
        address_text: address,
        reward_amount: parseFloat(form.reward_amount) || 0,
        contact_phone: form.contact_phone || null,
        photo_urls: photoUrls,
      };
      if (lat != null && lng != null) {
        payload.latitude = lat;
        payload.longitude = lng;
      }
      const res = await lostFoundAPI.create(payload);
      navigate(`/lost-found/${res.data.id}`);
    } catch (err) {
      setError(formatApiError(err, '发布失败，请检查表单后重试。'));
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="py-3">
      <nav aria-label="breadcrumb" className="mb-3">
        <ol className="breadcrumb">
          <li className="breadcrumb-item"><Link to="/lost-found">报失寻主</Link></li>
          <li className="breadcrumb-item active">发布信息</li>
        </ol>
      </nav>

      <h2 className="mb-4"><i className="fas fa-edit me-2 text-success"></i>发布报失/寻主信息</h2>

      {error && <div className="alert alert-danger">{error}</div>}

      <form onSubmit={handleSubmit} className="card shadow-sm">
        <div className="card-body">
          <div className="row g-3">
            <div className="col-md-6">
              <label className="form-label">类型</label>
              <select name="post_type" className="form-select" value={form.post_type} onChange={handleChange} required>
                <option value="lost">{LOST_FOUND_TYPE.lost}（丢失）</option>
                <option value="found">{LOST_FOUND_TYPE.found}（发现）</option>
              </select>
            </div>
            <div className="col-md-6">
              <label className="form-label">宠物种类</label>
              <input type="text" name="pet_species" className="form-control" value={form.pet_species} onChange={handleChange} required placeholder="如：中华田园猫" />
            </div>
            <div className="col-12">
              <label className="form-label">特征描述</label>
              <button type="button" className="btn btn-outline-success btn-sm mb-2" onClick={async () => {
                if (!photoUrls[0]) { alert('请先上传照片'); return; }
                try {
                  const res = await aiAPI.breedDetect({
                    image_url: photoUrls[0],
                    description: `${form.pet_species} ${form.features}`,
                  });
                  const parts = [
                    res.data.species && `物种：${res.data.species}`,
                    res.data.breed && `品种：${res.data.breed}`,
                    res.data.summary && res.data.summary !== '不确定' && `特征：${res.data.summary}`,
                  ].filter(Boolean);
                  setForm((f) => ({ ...f, features: parts.join('；') || res.data.result || f.features }));
                } catch (err) { alert(err.response?.data?.detail || 'AI 失败'); }
              }}>AI 识图辅助特征</button>
              <textarea name="features" className="form-control" rows={4} value={form.features} onChange={handleChange} required placeholder="毛色、体型、特殊标记等" />
            </div>
            <div className="col-12">
              <label className="form-label">事发地点</label>
              <input
                type="text"
                name="address_text"
                className="form-control"
                value={form.address_text}
                onChange={handleChange}
                required
                placeholder="如：XX 大学南门、XX 小区北门公交站"
              />
            </div>
            <div className="col-12">
              <label className="form-label">位置辅助（推荐）</label>
              <div className="d-flex flex-wrap align-items-center gap-2">
                <button
                  type="button"
                  className="btn btn-outline-success btn-sm"
                  onClick={handleUseCurrentLocation}
                  disabled={locating || submitting}
                >
                  {locating ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true" />
                      定位中...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-location-arrow me-1" />
                      使用当前位置
                    </>
                  )}
                </button>
                {hasCoordinates() && (
                  <span className="badge bg-light text-success border">
                    已记录坐标
                  </span>
                )}
              </div>
              {locationHint && <small className="text-muted d-block mt-2">{locationHint}</small>}
            </div>
            <div className="col-md-6">
              <label className="form-label">悬赏金额（元）</label>
              <input type="number" step="0.01" min="0" name="reward_amount" className="form-control" value={form.reward_amount} onChange={handleChange} />
            </div>
            <div className="col-md-6">
              <label className="form-label">联系电话</label>
              <input type="tel" name="contact_phone" className="form-control" value={form.contact_phone} onChange={handleChange} placeholder="可选" />
            </div>
            <div className="col-12">
              <label className="form-label">照片</label>
              <input type="file" className="form-control" accept="image/*" multiple onChange={handlePhotoUpload} disabled={uploading} />
              {uploading && <small className="text-muted">上传中...</small>}
              {photoUrls.length > 0 && (
                <div className="d-flex flex-wrap gap-2 mt-2">
                  {photoUrls.map((url, idx) => (
                    <div key={url} className="position-relative">
                      <img src={url} alt="" style={{ width: 80, height: 80, objectFit: 'cover', borderRadius: 8 }} />
                      <button type="button" className="btn btn-danger btn-sm position-absolute top-0 end-0" style={{ padding: '0 4px', fontSize: 10 }} onClick={() => removePhoto(idx)}>×</button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
        <div className="card-footer d-flex gap-2">
          <button type="submit" className="btn btn-success" disabled={submitting || uploading}>
            {submitting ? '提交中...' : '发布'}
          </button>
          <Link to="/lost-found" className="btn btn-outline-secondary">取消</Link>
        </div>
      </form>
    </div>
  );
};

export default LostFoundPublish;
