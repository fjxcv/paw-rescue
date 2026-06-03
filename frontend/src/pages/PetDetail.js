import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { adoptAPI, petsAPI, uploadAPI } from '../api/api';
import { ADOPTION_STATUS } from '../constants/site';

const SPECIES_LABELS = {
  dog: '狗',
  cat: '猫',
  bird: '鸟',
  rabbit: '兔',
  fish: '鱼',
  other: '其他',
};

const GENDER_LABELS = {
  male: '公',
  female: '母',
  unknown: '未知',
};

const formatAgeMonths = (months) => {
  if (months == null || months === '') return '未知';
  const m = Number(months);
  if (m < 12) return `${m}个月`;
  const years = Math.floor(m / 12);
  const rem = m % 12;
  if (rem === 0) return `${years}岁`;
  return `${years}岁${rem}个月`;
};

const ADOPTION_BADGE = {
  available: 'success',
  pending: 'warning text-dark',
  adopted: 'secondary',
};

const QUESTIONNAIRE_FIELDS = [
  { key: 'housing_type', label: '居住类型（公寓/独栋/其他）' },
  { key: 'has_other_pets', label: '是否已有其他宠物？（是/否）' },
  { key: 'experience', label: '养宠经验' },
  { key: 'daily_hours', label: '每日在家时长（小时）' },
  { key: 'family_agreement', label: '家人是否同意领养？（是/否）' },
];

const FILE_TYPE_LABELS = {
  id_card: '身份证',
  income_proof: '收入证明',
  housing_proof: '住房证明',
  other: '其他',
};

const PetDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [pet, setPet] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [adoptStep, setAdoptStep] = useState(1);
  const [applicationId, setApplicationId] = useState(null);
  const [message, setMessage] = useState('');
  const [questionnaire, setQuestionnaire] = useState(
    QUESTIONNAIRE_FIELDS.reduce((acc, f) => ({ ...acc, [f.key]: '' }), {})
  );
  const [attachmentFile, setAttachmentFile] = useState(null);
  const [fileType, setFileType] = useState('id_card');
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  useEffect(() => {
    const fetchPet = async () => {
      try {
        setLoading(true);
        const response = await petsAPI.getById(id);
        setPet(response.data);
      } catch (err) {
        setError('加载宠物详情失败，请稍后重试。');
        console.error('Error fetching pet:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchPet();
  }, [id]);

  const requireAuth = () => {
    if (!localStorage.getItem('token')) {
      navigate('/login');
      return false;
    }
    return true;
  };

  const handleStep1Submit = async (e) => {
    e.preventDefault();
    if (!requireAuth()) return;

    try {
      setSubmitting(true);
      setSubmitError(null);
      const response = await adoptAPI.create({
        pet_id: pet.id,
        message,
      });
      setApplicationId(response.data.id);
      setAdoptStep(2);
    } catch (err) {
      const detail = err.response?.data?.detail || err.response?.data?.non_field_errors?.[0];
      setSubmitError(detail || '提交领养申请失败，请重试。');
      console.error('Error creating application:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleStep2Submit = async (e) => {
    e.preventDefault();
    if (!requireAuth() || !applicationId) return;

    try {
      setSubmitting(true);
      setSubmitError(null);
      await adoptAPI.submitQuestionnaire(applicationId, questionnaire);
      setAdoptStep(3);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setSubmitError(detail || '提交问卷失败，请重试。');
      console.error('Error submitting questionnaire:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleStep3Submit = async (e) => {
    e.preventDefault();
    if (!requireAuth() || !applicationId || !attachmentFile) {
      setSubmitError('请选择要上传的文件。');
      return;
    }

    try {
      setSubmitting(true);
      setSubmitError(null);
      const uploadResponse = await uploadAPI.upload(attachmentFile, 'adopt');
      await adoptAPI.addAttachment(applicationId, {
        file_type: fileType,
        file_url: uploadResponse.data.url,
        file_size: attachmentFile.size,
      });
      setSubmitSuccess(true);
      setTimeout(() => navigate('/dashboard'), 2000);
    } catch (err) {
      setSubmitError('上传附件失败，请重试。');
      console.error('Error uploading attachment:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleQuestionnaireChange = (key, value) => {
    setQuestionnaire((prev) => ({ ...prev, [key]: value }));
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">加载中...</span>
        </div>
        <p className="mt-2">正在加载宠物详情...</p>
      </div>
    );
  }

  if (error || !pet) {
    return (
      <div className="alert alert-danger" role="alert">
        {error || '未找到该宠物。'}
      </div>
    );
  }

  const canAdopt = pet.adoption_status === 'available';

  return (
    <div className="container py-4">
      <div className="row">
        <div className="col-md-6 mb-4">
          <img
            src={pet.photo_url || 'https://via.placeholder.com/600x400?text=Pet+Photo'}
            className="img-fluid rounded shadow"
            alt={pet.name}
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/600x400?text=Pet+Photo';
            }}
          />
        </div>

        <div className="col-md-6">
          <h2 className="mb-3">{pet.name}</h2>
          <div className="mb-3">
            <p><strong>种类：</strong> {SPECIES_LABELS[pet.species] || pet.species}</p>
            <p><strong>品种：</strong> {pet.breed || '未知'}</p>
            <p><strong>年龄：</strong> {formatAgeMonths(pet.age_months)}</p>
            <p><strong>性别：</strong> {GENDER_LABELS[pet.gender] || pet.gender || '未知'}</p>
            <p><strong>健康状况：</strong> {pet.health_status || '未填写'}</p>
            <p>
              <strong>领养状态：</strong>{' '}
              <span className={`badge bg-${ADOPTION_BADGE[pet.adoption_status] || 'secondary'}`}>
                {ADOPTION_STATUS[pet.adoption_status] || pet.adoption_status}
              </span>
            </p>
            {pet.rescue_case && (
              <p><strong>关联救助案例：</strong> #{pet.rescue_case}</p>
            )}
            <p><strong>描述：</strong></p>
            <p className="text-muted">{pet.description || '暂无描述。'}</p>
          </div>

          {canAdopt ? (
            <div className="card shadow-sm">
              <div className="card-header bg-primary text-white">
                <h5 className="mb-0">领养申请</h5>
                <small>第 {adoptStep} 步，共 3 步</small>
              </div>
              <div className="card-body">
                <div className="progress mb-3" style={{ height: '8px' }}>
                  <div
                    className="progress-bar bg-success"
                    style={{ width: `${(adoptStep / 3) * 100}%` }}
                  ></div>
                </div>

                {submitSuccess ? (
                  <div className="alert alert-success">
                    申请提交成功！正在跳转到个人中心...
                  </div>
                ) : (
                  <>
                    {adoptStep === 1 && (
                      <form onSubmit={handleStep1Submit}>
                        <p className="text-muted small">第 1 步：填写领养留言</p>
                        <div className="mb-3">
                          <label htmlFor="message" className="form-label">
                            您为什么想领养 {pet.name}？
                          </label>
                          <textarea
                            id="message"
                            className="form-control"
                            rows="4"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            placeholder="请介绍您的领养意愿和养宠条件..."
                            required
                          />
                        </div>
                        {submitError && <div className="alert alert-danger">{submitError}</div>}
                        <button type="submit" className="btn btn-primary" disabled={submitting}>
                          {submitting ? '提交中...' : '下一步：填写问卷'}
                        </button>
                      </form>
                    )}

                    {adoptStep === 2 && (
                      <form onSubmit={handleStep2Submit}>
                        <p className="text-muted small">第 2 步：完成领养问卷</p>
                        {QUESTIONNAIRE_FIELDS.map((field) => (
                          <div className="mb-3" key={field.key}>
                            <label className="form-label">{field.label}</label>
                            <input
                              type="text"
                              className="form-control"
                              value={questionnaire[field.key]}
                              onChange={(e) => handleQuestionnaireChange(field.key, e.target.value)}
                              required
                            />
                          </div>
                        ))}
                        {submitError && <div className="alert alert-danger">{submitError}</div>}
                        <div className="d-flex gap-2">
                          <button
                            type="button"
                            className="btn btn-outline-secondary"
                            onClick={() => setAdoptStep(1)}
                            disabled={submitting}
                          >
                            上一步
                          </button>
                          <button type="submit" className="btn btn-primary" disabled={submitting}>
                            {submitting ? '提交中...' : '下一步：上传材料'}
                          </button>
                        </div>
                      </form>
                    )}

                    {adoptStep === 3 && (
                      <form onSubmit={handleStep3Submit}>
                        <p className="text-muted small">第 3 步：上传证明材料</p>
                        <div className="mb-3">
                          <label className="form-label">材料类型</label>
                          <select
                            className="form-select"
                            value={fileType}
                            onChange={(e) => setFileType(e.target.value)}
                          >
                            {Object.entries(FILE_TYPE_LABELS).map(([value, label]) => (
                              <option key={value} value={value}>{label}</option>
                            ))}
                          </select>
                        </div>
                        <div className="mb-3">
                          <label className="form-label">上传文件</label>
                          <input
                            type="file"
                            className="form-control"
                            accept="image/*,.pdf"
                            onChange={(e) => setAttachmentFile(e.target.files?.[0] || null)}
                            required
                          />
                          <small className="text-muted">支持 JPG、PNG、GIF、WEBP 或 PDF</small>
                        </div>
                        {submitError && <div className="alert alert-danger">{submitError}</div>}
                        <div className="d-flex gap-2">
                          <button
                            type="button"
                            className="btn btn-outline-secondary"
                            onClick={() => setAdoptStep(2)}
                            disabled={submitting}
                          >
                            上一步
                          </button>
                          <button type="submit" className="btn btn-success" disabled={submitting}>
                            {submitting ? '上传中...' : '提交申请'}
                          </button>
                        </div>
                      </form>
                    )}
                  </>
                )}
              </div>
            </div>
          ) : (
            <div className="alert alert-info">
              该宠物当前不可领养（状态：{ADOPTION_STATUS[pet.adoption_status] || pet.adoption_status}）。
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PetDetail;
