# -*- coding: utf-8 -*-
import os

ROOT = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'src', 'pages')

def w(name, content):
    path = os.path.join(ROOT, name)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('fixed', name)

DASHBOARD = r'''import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { adoptAPI } from '../api/api';
import { ONLINE_STATUS } from '../constants/site';

const STATUS_BADGE = {
  pending: 'bg-warning text-dark',
  approved: 'bg-success',
  rejected: 'bg-danger',
  need_material: 'bg-info text-dark',
};

const SPECIES_LABELS = { dog: '\u72d7', cat: '\u732b', bird: '\u9e1f', rabbit: '\u5154', fish: '\u9c7c', other: '\u5176\u4ed6' };

const formatAgeMonths = (months) => {
  if (months == null) return '\u672a\u77e5';
  const m = Number(months);
  if (m < 12) return `${m}\u4e2a\u6708`;
  const y = Math.floor(m / 12);
  const r = m % 12;
  return r === 0 ? `${y}\u5c81` : `${y}\u5c81${r}\u4e2a\u6708`;
};

const Dashboard = () => {
  const navigate = useNavigate();
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!localStorage.getItem('token')) { navigate('/login'); return; }
    (async () => {
      try {
        setLoading(true);
        const res = await adoptAPI.getMy();
        setApplications(Array.isArray(res.data) ? res.data : res.data.results || []);
      } catch (err) {
        setError('\u52a0\u8f7d\u9886\u517b\u7533\u8bf7\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5\u3002');
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, [navigate]);

  const getStatusBadge = (status) => {
    const label = ONLINE_STATUS[status] || status || '\u672a\u77e5';
    const badge = STATUS_BADGE[status] || 'bg-secondary';
    return <span className={`badge ${badge}`}>{label}</span>;
  };

  if (loading) return (
    <div className="text-center py-5">
      <div className="spinner-border text-primary" role="status"></div>
      <p className="mt-2">\u52a0\u8f7d\u4e2d...</p>
    </div>
  );
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container py-4">
      <h2 className="mb-4"><i className="fas fa-tachometer-alt me-2"></i>\u6211\u7684\u9886\u517b</h2>
      <div className="row">
        <div className="col-md-8">
          <div className="card shadow-sm">
            <div className="card-header"><h5 className="mb-0">\u9886\u517b\u7533\u8bf7\u8bb0\u5f55</h5></div>
            <div className="card-body">
              {applications.length === 0 ? (
                <p className="text-muted mb-0">\u6682\u65e0\u9886\u517b\u7533\u8bf7\u3002\u53bb <a href="/pets">\u9886\u517b\u5ba0\u7269</a> \u9875\u9762\u63d0\u4ea4\u7533\u8bf7\u5427\u3002</p>
              ) : (
                <div className="list-group list-group-flush">
                  {applications.map((app) => (
                    <div key={app.id} className="list-group-item px-0">
                      <div className="d-flex justify-content-between align-items-start">
                        <div className="flex-grow-1">
                          <h6 className="mb-1">{app.pet?.name || '\u672a\u547d\u540d'}</h6>
                          {app.pet && (
                            <p className="mb-1 small text-muted">
                              {SPECIES_LABELS[app.pet.species] || app.pet.species} \u00b7 {app.pet.breed || '\u672a\u77e5'} \u00b7 {formatAgeMonths(app.pet.age_months)}
                            </p>
                          )}
                          <p className="mb-1"><strong>\u7559\u8a00\uff1a</strong>{app.message || '\u65e0'}</p>
                          {app.audit_opinion && <p className="mb-1 small"><strong>\u5ba1\u6838\u610f\u89c1\uff1a</strong>{app.audit_opinion}</p>}
                          <small className="text-muted">\u7533\u8bf7\u65f6\u95f4\uff1a{app.created_at ? new Date(app.created_at).toLocaleDateString() : '-'}</small>
                        </div>
                        <div className="ms-3">{getStatusBadge(app.online_status)}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card shadow-sm">
            <div className="card-header"><h5 className="mb-0">\u5feb\u6377\u64cd\u4f5c</h5></div>
            <div className="card-body d-grid gap-2">
              <button type="button" className="btn btn-primary" onClick={() => navigate('/pets')}>\u6d4f\u89c8\u5ba0\u7269</button>
              <button type="button" className="btn btn-outline-primary" onClick={() => navigate('/community')}>\u4e92\u52a8\u793e\u533a</button>
              <button type="button" className="btn btn-outline-secondary" onClick={() => navigate('/profile')}>\u4e2a\u4eba\u8d44\u6599</button>
            </div>
          </div>
          <div className="card shadow-sm mt-3">
            <div className="card-header"><h6 className="mb-0">\u72b6\u6001\u8bf4\u660e</h6></div>
            <div className="card-body small">
              <p className="mb-1">{getStatusBadge('pending')} \u5f85\u5ba1\u6838</p>
              <p className="mb-1">{getStatusBadge('approved')} \u5df2\u901a\u8fc7</p>
              <p className="mb-1">{getStatusBadge('rejected')} \u5df2\u62d2\u7edd</p>
              <p className="mb-0">{getStatusBadge('need_material')} \u9700\u8865\u5145\u6750\u6599</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Dashboard;
'''

RESCUE_LIST = r'''import React, { useEffect, useState } from 'react';
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
        setError('\u52a0\u8f7d\u6551\u52a9\u6848\u4f8b\u5931\u8d25\u3002');
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div className="py-3">
      <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
        <h2><i className="fas fa-hand-holding-heart me-2 text-success"></i>\u6551\u52a9\u8ffd\u8e2a</h2>
        <Link to="/rescue/report" className="btn btn-success"><i className="fas fa-plus me-1"></i>\u4e0a\u62a5\u6551\u52a9</Link>
      </div>
      {loading && <div className="text-center py-5"><div className="spinner-border text-success"></div><p className="mt-2">\u52a0\u8f7d\u4e2d...</p></div>}
      {error && <div className="alert alert-danger">{error}</div>}
      {!loading && !error && (
        <div className="row">
          {cases.length === 0 ? (
            <div className="col-12 text-center text-muted py-5">\u6682\u65e0\u6551\u52a9\u8bb0\u5f55</div>
          ) : cases.map((item) => (
            <div key={item.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100 shadow-sm">
                {item.photo_urls?.[0] && <img src={item.photo_urls[0]} className="card-img-top" alt="" style={{height:'180px',objectFit:'cover'}} />}
                <div className="card-body">
                  <span className="badge bg-primary me-2">{item.rescue_no}</span>
                  <span className="badge bg-secondary">{RESCUE_STATUS[item.current_status] || item.current_status}</span>
                  <p className="card-text small text-muted mt-2">{item.appearance?.slice(0,100) || '\u65e0\u63cf\u8ff0'}</p>
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
'''

# decode unicode escapes in file content
def decode_content(s):
    return s.encode('utf-8').decode('unicode_escape')

if __name__ == '__main__':
    w('Dashboard.js', decode_content(DASHBOARD))
    w('RescueList.js', decode_content(RESCUE_LIST))
