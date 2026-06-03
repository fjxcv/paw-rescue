import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { rescueAPI, uploadAPI } from '../api/api';
import { formatApiError, roundCoordinate } from '../utils/apiError';

const RescueReport = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    discover_latitude: '',
    discover_longitude: '',
    discover_address: '',
    appearance: '',
    health_note: '',
  });
  const [photoUrls, setPhotoUrls] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [locating, setLocating] = useState(false);
  const [locationHint, setLocationHint] = useState('');
  const [error, setError] = useState('');

  const hasCoordinates = () => {
    const lat = parseFloat(form.discover_latitude);
    const lng = parseFloat(form.discover_longitude);
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
          discover_latitude: String(roundCoordinate(pos.coords.latitude)),
          discover_longitude: String(roundCoordinate(pos.coords.longitude)),
        }));
        const meters = Math.round(pos.coords.accuracy);
        setLocationHint(`已记录当前位置（定位精度约 ${meters} 米）`);
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
        const res = await uploadAPI.upload(file, 'rescue');
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
    const address = form.discover_address.trim();
    if (!address) {
      setError('请填写发现地点或附近地标。');
      return;
    }
    setSubmitting(true);
    setError('');
    try {
      const lat = roundCoordinate(form.discover_latitude);
      const lng = roundCoordinate(form.discover_longitude);
      const payload = {
        discover_address: address,
        appearance: form.appearance,
        health_note: form.health_note,
        photo_urls: photoUrls,
      };
      if (lat != null && lng != null) {
        payload.discover_latitude = lat;
        payload.discover_longitude = lng;
      }
      await rescueAPI.create(payload);
      navigate('/rescue');
    } catch (err) {
      setError(formatApiError(err, '上报失败，请检查表单后重试。'));
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="py-3">
      <nav aria-label="breadcrumb" className="mb-3">
        <ol className="breadcrumb">
          <li className="breadcrumb-item"><Link to="/rescue">救助追踪</Link></li>
          <li className="breadcrumb-item active">上报救助</li>
        </ol>
      </nav>

      <h2 className="mb-4"><i className="fas fa-hand-holding-heart me-2 text-success"></i>上报救助案例</h2>

      {error && <div className="alert alert-danger">{error}</div>}

      <form onSubmit={handleSubmit} className="card shadow-sm">
        <div className="card-body">
          <div className="row g-3">
            <div className="col-12">
              <label className="form-label">发现地点</label>
              <input
                type="text"
                name="discover_address"
                className="form-control"
                value={form.discover_address}
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
            <div className="col-12">
              <label className="form-label">外观描述</label>
              <textarea name="appearance" className="form-control" rows={3} value={form.appearance} onChange={handleChange} placeholder="品种、毛色、体型等" />
            </div>
            <div className="col-12">
              <label className="form-label">健康状况</label>
              <textarea name="health_note" className="form-control" rows={3} value={form.health_note} onChange={handleChange} placeholder="受伤情况、精神状态等" />
            </div>
            <div className="col-12">
              <label className="form-label">现场照片</label>
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
            {submitting ? '提交中...' : '提交上报'}
          </button>
          <Link to="/rescue" className="btn btn-outline-secondary">取消</Link>
        </div>
      </form>
    </div>
  );
};

export default RescueReport;
