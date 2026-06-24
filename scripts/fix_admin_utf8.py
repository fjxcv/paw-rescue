# -*- coding: utf-8 -*-
"""Fix admin UI UTF-8 / mojibake and LostFound reward label."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fix_file_mojibake(path: Path) -> bool:
    try:
        text = path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return False
    original = text

    def try_fix_string(match_text: str) -> str:
        try:
            fixed = match_text.encode('latin1').decode('gbk')
            if fixed != match_text and any('\u4e00' <= c <= '\u9fff' for c in fixed):
                return fixed
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        return match_text

    # Fix quoted strings that look like GBK-read-as-UTF-8
    import re

    def repl(m):
        s = m.group(1)
        fixed = try_fix_string(s)
        return f"'{fixed}'"

    text = re.sub(r"'((?:\\'|[^'])*)'", repl, text)

    def repl_d(m):
        s = m.group(1)
        fixed = try_fix_string(s)
        return f'"{fixed}"'

    text = re.sub(r'"((?:\\"|[^"])*)"', repl_d, text)

    if text != original:
        path.write_text(text, encoding='utf-8', newline='\n')
        return True
    return False


def write_admin_route():
    content = '''import React, { useEffect, useState } from 'react';
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
        setError(err.response?.data?.detail || '\u65e0\u6cd5\u9a8c\u8bc1\u7ba1\u7406\u5458\u6743\u9650');
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
        <p className="mt-2">\u6b63\u5728\u9a8c\u8bc1\u7ba1\u7406\u5458\u6743\u9650...</p>
      </div>
    );
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  if (!isAdminUser(user)) {
    return (
      <div className="alert alert-warning">
        \u60a8\u6ca1\u6709\u7ba1\u7406\u5458\u6743\u9650\u3002
        <Link to="/" className="ms-2">\u8fd4\u56de\u9996\u9875</Link>
      </div>
    );
  }

  return children;
};

export default AdminRoute;
'''
    path = ROOT / 'frontend/src/components/AdminRoute.js'
    path.write_text(content, encoding='utf-8', newline='\n')
    print('Wrote', path.name)


def fix_lostfound_reward_label():
    path = ROOT / 'frontend/src/pages/LostFoundList.js'
    text = path.read_text(encoding='utf-8')
    text = text.replace('\u4ec5\u770b\u6709\u60ac\u8d44', '\u4ec5\u770b\u6709\u8d4f\u91d1')
    path.write_text(text, encoding='utf-8', newline='\n')
    print('Fixed LostFoundList reward label')


def main():
    import subprocess
    import sys
    subprocess.run([sys.executable, str(ROOT / 'scripts/ensure_utf8.py')], check=False)

    from write_utf8_sources import write_site_js
    write_site_js()
    write_admin_route()
    fix_lostfound_reward_label()
    admin_files = [
        ROOT / 'frontend/src/pages/AdminDashboard.js',
        ROOT / 'frontend/src/components/CarouselAdminPanel.js',
        ROOT / 'frontend/src/components/AdminManageBar.js',
    ]
    for path in admin_files:
        if path.exists() and fix_file_mojibake(path):
            print('Fixed mojibake in', path.name)


if __name__ == '__main__':
    main()
