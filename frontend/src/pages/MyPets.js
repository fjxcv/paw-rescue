import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI, rescueAPI } from '../api/api';
import { RESCUE_STATUS } from '../constants/site';

const MyPets = () => {
  const navigate = useNavigate();
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!localStorage.getItem('token')) {
      navigate('/login');
      return;
    }
    fetchMyRescues();
  }, [navigate]);

  const fetchMyRescues = async () => {
    try {
      setLoading(true);
      const [profileRes, rescueRes] = await Promise.all([
        authAPI.getProfile(),
        rescueAPI.getAll(),
      ]);
      const userId = profileRes.data.id;
      setCases((rescueRes.data || []).filter((item) => item.reporter?.id === userId));
    } catch (err) {
      setError('加载您的救助上报失败。');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-success" role="status">
          <span className="visually-hidden">加载中...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  return (
    <div className="container py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2><i className="fas fa-heart me-2 text-danger"></i>我的救助上报</h2>
        <Link to="/rescue/report" className="btn btn-success">上报救助</Link>
      </div>

      {cases.length === 0 ? (
        <div className="text-center py-5 text-muted">
          <p>暂无救助上报记录。</p>
          <Link to="/rescue/report" className="btn btn-outline-success">提交第一条上报</Link>
        </div>
      ) : (
        <div className="row">
          {cases.map((item) => (
            <div key={item.id} className="col-md-6 mb-3">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">{item.rescue_no}</h5>
                  <p className="mb-1"><strong>状态：</strong> {RESCUE_STATUS[item.current_status] || item.current_status}</p>
                  <p className="mb-1"><strong>地点：</strong> {item.discover_address || '未填写'}</p>
                  <p className="text-muted small">{item.appearance}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MyPets;
