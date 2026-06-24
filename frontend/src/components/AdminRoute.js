import React, { useEffect, useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { authAPI } from '../api/api';

export const isAdminUser = (user) => {
  const role = user?.profile?.role;
  return role === 'admin' || user?.is_superuser || user?.is_staff;
};

const AdminRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(!!token);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!token) return;
    (async () => {
      try {
        const res = await authAPI.getProfile();
        setUser(res.data);
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.removeItem('token');
        }
        setError(err.response?.data?.detail || '无法验证管理员权限');
      } finally {
        setLoading(false);
      }
    })();
  }, [token]);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-primary" role="status"></div>
        <p className="mt-2">正在验证管理员权限...</p>
      </div>
    );
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  if (!isAdminUser(user)) {
    return (
      <div className="alert alert-warning">
        您没有管理员权限。
        <Link to="/" className="ms-2">返回首页</Link>
      </div>
    );
  }

  return children;
};

export default AdminRoute;
