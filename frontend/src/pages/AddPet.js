import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { aiAPI, authAPI, petsAPI, rescueAPI, uploadAPI } from '../api/api';

const AddPet = () => {
  const navigate = useNavigate();
  const [authorized, setAuthorized] = useState(false);
  const [authChecking, setAuthChecking] = useState(true);
  const [rescueCases, setRescueCases] = useState([]);
  const [form, setForm] = useState({
    name: '',
    species: '',
    breed: '',
    age_months: '',
    gender: 'unknown',
    health_status: '',
    description: '',
    photo_url: '',
    is_public: true,
    rescue_case: '',
  });
  const [photoUploading, setPhotoUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const checkAdmin = async () => {
      try {
        const response = await authAPI.getProfile();
        if (response.data.profile?.role !== 'admin') {
          navigate('/pets');
          return;
        }
        setAuthorized(true);
        const casesResponse = await rescueAPI.getAll();
        const cases = Array.isArray(casesResponse.data)
          ? casesResponse.data
          : casesResponse.data.results || [];
        setRescueCases(cases);
      } catch (err) {
        console.error('Auth check failed:', err);
        navigate('/login');
      } finally {
        setAuthChecking(false);
      }
    };
    checkAdmin();
  }, [navigate]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handlePhotoChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setPhotoUploading(true);
      const response = await uploadAPI.upload(file, 'pets');
      setForm((prev) => ({ ...prev, photo_url: response.data.url }));
    } catch (err) {
      setError('照片上传失败，请重试。');
      console.error(err);
    } finally {
      setPhotoUploading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);
    try {
      const payload = {
        name: form.name,
        species: form.species,
        breed: form.breed || null,
        age_months: form.age_months ? Number(form.age_months) : null,
        gender: form.gender,
        health_status: form.health_status || null,
        description: form.description || null,
        photo_url: form.photo_url || null,
        is_public: form.is_public,
        adoption_status: 'available',
      };
      if (form.rescue_case) payload.rescue_case = Number(form.rescue_case);
      await petsAPI.create(payload);
      setSuccess(true);
      setTimeout(() => navigate('/pets'), 1500);
    } catch (err) {
      setError('添加宠物档案失败，请重试。');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (authChecking) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-success" role="status"></div>
        <p className="mt-2">验证权限中...</p>
      </div>
    );
  }

  if (!authorized) return null;

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-7">
          <div className="card shadow-lg border-0">
            <div className="card-header bg-success text-white text-center">
              <h3><i className="fas fa-plus-circle me-2"></i>添加宠物档案</h3>
            </div>
            <div className="card-body p-4">
              <form onSubmit={handleSubmit}>
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label fw-bold">宠物名称 *</label>
                    <input type="text" className="form-control" name="name" value={form.name} onChange={handleChange} required placeholder="例如：小橘" />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label fw-bold">物种 *</label>
                    <select className="form-select" name="species" value={form.species} onChange={handleChange} required>
                      <option value="">请选择</option>
                      <option value="dog">狗</option>
                      <option value="cat">猫</option>
                      <option value="bird">鸟</option>
                      <option value="rabbit">兔</option>
                      <option value="fish">鱼</option>
                      <option value="other">其他</option>
                    </select>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label fw-bold">品种</label>
                    <input type="text" className="form-control" name="breed" value={form.breed} onChange={handleChange} placeholder="例如：田园猫" />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label fw-bold">月龄</label>
                    <input type="number" className="form-control" name="age_months" value={form.age_months} onChange={handleChange} min="0" max="360" placeholder="例如：12" />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label fw-bold">性别</label>
                    <select className="form-select" name="gender" value={form.gender} onChange={handleChange}>
                      <option value="unknown">未知</option>
                      <option value="male">公</option>
                      <option value="female">母</option>
                    </select>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label fw-bold">健康状况</label>
                    <input type="text" className="form-control" name="health_status" value={form.health_status} onChange={handleChange} placeholder="例如：已驱虫疫苗" />
                  </div>
                  <div className="col-md-12">
                    <label className="form-label fw-bold">描述</label>
                    <div className="mb-2">
                      <button type="button" className="btn btn-outline-success btn-sm me-2" onClick={async () => {
                        try {
                          if (!form.photo_url) { alert('请先上传宠物照片'); return; }
                          const res = await aiAPI.breedDetect({ image_url: form.photo_url, description: `${form.species} ${form.breed}` });
                          const breedLabel = res.data.breed || '';
                          const speciesLabel = (res.data.species || '').toLowerCase();
                          let speciesValue = form.species;
                          if (speciesLabel.includes('猫')) speciesValue = 'cat';
                          else if (speciesLabel.includes('狗')) speciesValue = 'dog';
                          const note = res.data.summary ? `备注：${res.data.summary}` : '';
                          setForm((f) => ({
                            ...f,
                            species: speciesValue || f.species,
                            breed: breedLabel.slice(0, 40) || f.breed,
                            description: f.description || note,
                          }));
                        } catch (err) { alert(err.response?.data?.detail || 'AI 失败'); }
                      }}>AI 识别品种</button>
                      <button type="button" className="btn btn-outline-primary btn-sm" onClick={async () => {
                        try {
                          const res = await aiAPI.adoptCopy({ pet_name: form.name, species: form.species, breed: form.breed, description: form.description });
                          setForm((f) => ({ ...f, description: res.data.copy }));
                        } catch (err) { alert(err.response?.data?.detail || 'AI 失败'); }
                      }}>AI 生成领养文案</button>
                    </div>
                    <textarea className="form-control" name="description" value={form.description} onChange={handleChange} rows="4" placeholder="性格、习惯、注意事项等..." />
                  </div>
                  <div className="col-md-12">
                    <label className="form-label fw-bold">照片</label>
                    <input type="file" className="form-control" accept="image/*" onChange={handlePhotoChange} disabled={photoUploading} />
                    {photoUploading && <small className="text-muted">上传中...</small>}
                    {form.photo_url && (
                      <div className="mt-2">
                        <img src={form.photo_url} alt="预览" className="img-thumbnail" style={{ maxHeight: '120px' }} />
                      </div>
                    )}
                  </div>
                  <div className="col-md-6">
                    <label className="form-label fw-bold">关联救助案例</label>
                    <select className="form-select" name="rescue_case" value={form.rescue_case} onChange={handleChange}>
                      <option value="">无</option>
                      {rescueCases.map((c) => (
                        <option key={c.id} value={c.id}>
                          {c.rescue_no || `案例 #${c.id}`}
                          {c.discover_address ? ` - ${c.discover_address}` : ''}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="col-md-6 d-flex align-items-end">
                    <div className="form-check">
                      <input type="checkbox" className="form-check-input" id="is_public" name="is_public" checked={form.is_public} onChange={handleChange} />
                      <label className="form-check-label" htmlFor="is_public">公开显示</label>
                    </div>
                  </div>
                </div>

                {error && <div className="alert alert-danger mt-3">{error}</div>}
                {success && <div className="alert alert-success mt-3">添加成功，正在跳转...</div>}

                <div className="d-grid gap-2 mt-4">
                  <button type="submit" className="btn btn-success btn-lg" disabled={loading || photoUploading}>
                    {loading ? '提交中...' : '提交档案'}
                  </button>
                  <button type="button" className="btn btn-outline-secondary" onClick={() => navigate('/pets')} disabled={loading}>
                    返回列表
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddPet;
