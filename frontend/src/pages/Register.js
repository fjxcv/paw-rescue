import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../api/api';
import { SITE_NAME } from '../constants/site';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    has_privacy_consent: false,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.has_privacy_consent) {
      setError('注册前须同意隐私政策。');
      return;
    }

    if (formData.password.length < 8) {
      setError('密码长度至少 8 位。');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await authAPI.register(formData);
      alert(`欢迎加入 ${SITE_NAME}！请登录。`);
      navigate('/login');
    } catch (err) {
      console.error('Registration error details:', err);

      if (err.response) {
        const status = err.response.status;
        const data = err.response.data;

        if (status === 400) {
          if (data.username) {
            setError(`用户名问题：${data.username[0]}`);
          } else if (data.email) {
            setError(`邮箱问题：${data.email[0]}`);
          } else if (data.password) {
            setError(`密码问题：${data.password[0]}`);
          } else if (data.has_privacy_consent) {
            setError(`隐私同意：${data.has_privacy_consent[0]}`);
          } else {
            setError('注册信息无效，请检查后重试。');
          }
        } else if (status === 409) {
          setError('该用户名已被占用，请换一个。');
        } else {
          setError(`注册失败（${status}），请稍后重试。`);
        }
      } else if (err.request) {
        setError('服务器无响应，请检查网络连接。');
      } else {
        setError('注册失败，请重试。');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="row justify-content-center" style={{ backgroundColor: '#fdf6f0', minHeight: '100vh', padding: '2rem' }}>
      <div className="col-md-6 col-lg-4">
        <div className="card shadow-sm border-0" style={{ borderRadius: '20px' }}>
          <div className="card-header text-center bg-light" style={{ borderRadius: '20px 20px 0 0' }}>
            <h3 className="text-primary">加入 {SITE_NAME}</h3>
          </div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="username" className="form-label fw-bold">用户名</label>
                <input
                  type="text"
                  className="form-control"
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  placeholder="例如：爱宠小助手"
                />
              </div>

              <div className="mb-3">
                <label htmlFor="email" className="form-label">邮箱地址</label>
                <input
                  type="email"
                  className="form-control"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  placeholder="yourname@example.com"
                />
              </div>

              <div className="mb-3">
                <label htmlFor="password" className="form-label">设置密码</label>
                <input
                  type="password"
                  className="form-control"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  minLength={8}
                  placeholder="至少 8 位字符"
                />
              </div>

              <div className="mb-3 form-check">
                <input
                  type="checkbox"
                  className="form-check-input"
                  id="has_privacy_consent"
                  name="has_privacy_consent"
                  checked={formData.has_privacy_consent}
                  onChange={handleChange}
                  required
                />
                <label className="form-check-label" htmlFor="has_privacy_consent">
                  我已阅读并同意隐私政策及数据处理条款 *
                </label>
              </div>

              {error && (
                <div className="alert alert-danger" role="alert">
                  {error}
                </div>
              )}

              <button
                type="submit"
                className="btn btn-success w-100"
                disabled={loading}
              >
                {loading ? '注册中...' : '创建账号'}
              </button>
            </form>

            <div className="text-center mt-3">
              <p>
                已有账号？{' '}
                <Link to="/login" className="text-decoration-none">立即登录</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
