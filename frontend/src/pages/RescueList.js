import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { rescueAPI } from '../api/api';
import { RESCUE_STATUS } from '../constants/site';

const RescueList = () => {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const res = await rescueAPI.getAll();
        setCases(res.data);
      } catch (err) {
        setError('加载救助案例失败。');
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div className="py-3">
      <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
        <h2><i className="fas fa-hand-holding-heart me-2 text-success"></i>救助追踪</h2>
        <Link to="/rescue/report" className="btn btn-success"><i className="fas fa-plus me-1"></i>上报救助</Link>
      </div>
      {loading && <div className="text-center py-5"><div className="spinner-border text-success"></div><p className="mt-2">加载中...</p></div>}
      {error && <div className="alert alert-danger">{error}</div>}
      {!loading && !error && (
        <div className="row">
          {cases.length === 0 ? (
            <div className="col-12 text-center text-muted py-5">暂无救助记录</div>
          ) : cases.map((item) => (
            <div key={item.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100 shadow-sm">
                {item.photo_urls?.[0] && <img src={item.photo_urls[0]} className="card-img-top" alt="" style={{height:'180px',objectFit:'cover'}} />}
                <div className="card-body">
                  <span className="badge bg-primary me-2">{item.rescue_no}</span>
                  <span className="badge bg-secondary">{RESCUE_STATUS[item.current_status] || item.current_status}</span>
                  <p className="card-text small text-muted mt-2">{item.appearance?.slice(0,100) || '无描述'}</p>
                  {item.discover_address && <p className="small"><i className="fas fa-map-marker-alt me-1"></i>{item.discover_address}</p>}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
export default RescueList;
