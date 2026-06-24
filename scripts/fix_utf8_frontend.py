# -*- coding: utf-8 -*-
import json
import os

ROOT = os.path.join(os.path.dirname(__file__), '..', 'frontend')
SN = '\u6696\u722a\u6551\u52a9'


def w(rel, content):
    path = os.path.join(ROOT, rel.replace('/', os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('OK', rel)


def main():
    w('src/constants/site.js', (
        'export const SITE_NAME = %r;\n\n' % SN
        + 'export const ADOPTION_STATUS = {available:%r,pending:%r,adopted:%r};\n' % (
            '\u53ef\u9886\u517b', '\u7533\u8bf7\u4e2d', '\u5df2\u9886\u517b')
        + 'export const ONLINE_STATUS = {pending:%r,approved:%r,rejected:%r,need_material:%r};\n' % (
            '\u5f85\u5ba1\u6838', '\u5df2\u901a\u8fc7', '\u5df2\u62d2\u7edd', '\u9700\u8865\u6750\u6599')
        + 'export const ARTICLE_TYPES = {science:%r,announcement:%r,law:%r,rescue_case:%r};\n' % (
            '\u79d1\u666e', '\u516c\u544a', '\u6cd5\u89c4', '\u6551\u52a9\u6848\u4f8b')
        + 'export const POST_CATEGORIES = {general:%r,rescue_share:%r,help_request:%r,pet_experience:%r};\n' % (
            '\u7efc\u5408', '\u6551\u52a9\u5206\u4eab', '\u6c42\u52a9', '\u517b\u5ba0\u7ecf\u9a8c')
        + 'export const LOST_FOUND_TYPE = {lost:%r,found:%r};\n' % ('\u5bfb\u5ba0', '\u62db\u9886')
        + 'export const RESCUE_STATUS = {pending_rescue:%r,in_medical:%r,recovering:%r,awaiting_adoption:%r,rescued:%r,abandoned:%r};\n' % (
            '\u5f85\u6551\u52a9', '\u533b\u7597\u4e2d', '\u5eb7\u590d\u4e2d', '\u5f85\u9886\u517b', '\u5df2\u6551\u52a9', '\u5df2\u7ec8\u6b62')
    ))

    w('public/index.html', (
        '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n'
        '<meta charset="utf-8" />\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1" />\n'
        '<meta name="description" content="%s - \u6d41\u6d6a\u5ba0\u7269\u7efc\u5408\u6551\u52a9\u7ba1\u7406\u5e73\u53f0" />\n'
        '<title>%s</title>\n'
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" crossorigin="anonymous" />\n'
        '</head>\n<body><noscript>\u8bf7\u542f\u7528 JavaScript\u3002</noscript><div id="root"></div></body></html>\n'
    ) % (SN, SN))

    manifest = {
        'short_name': SN,
        'name': SN + ' - \u6d41\u6d6a\u5ba0\u7269\u7efc\u5408\u6551\u52a9\u7ba1\u7406\u5e73\u53f0',
        'start_url': '.', 'display': 'standalone', 'theme_color': '#ff8c00', 'background_color': '#ffffff',
        'icons': [{'src': 'favicon.ico', 'sizes': '64x64', 'type': 'image/x-icon'}],
    }
    w('public/manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

    footer = '''import React from 'react';
import { Link } from 'react-router-dom';
import { SITE_NAME } from '../constants/site';

const Footer = () => (
  <footer className="footer-gradient text-white py-5 mt-auto">
    <div className="container">
      <div className="row mb-4 text-start text-md-center">
        <div className="col-md-4 mb-4 mb-md-0">
          <h5 className="fw-bold mb-3">%s</h5>
          <p className="mb-2"><i className="fas fa-map-marker-alt me-2 text-warning"></i>%s</p>
          <p className="mb-2"><i className="fas fa-phone me-2 text-warning"></i>400-888-0628\uFF08\u5de5\u4f5c\u65e5 9:00-18:00\uFF09</p>
          <p><i className="fas fa-envelope me-2 text-warning"></i>service@nuanzhao-rescue.cn</p>
        </div>
        <div className="col-md-4 mb-4 mb-md-0">
          <h5 className="fw-bold mb-3">%s</h5>
          <div className="d-flex flex-column gap-2 align-items-md-center">
            <Link to="/pets" className="footer-link text-white">%s</Link>
            <Link to="/cms" className="footer-link text-white">%s</Link>
            <Link to="/lost-found" className="footer-link text-white">%s</Link>
            <Link to="/community" className="footer-link text-white">%s</Link>
          </div>
        </div>
        <div className="col-md-4">
          <h5 className="fw-bold mb-3">%s</h5>
          <div className="d-flex justify-content-md-center gap-4">
            <button type="button" className="btn btn-link text-white p-0"><i className="fab fa-weixin fa-2x"></i></button>
            <button type="button" className="btn btn-link text-white p-0"><i className="fab fa-weibo fa-2x"></i></button>
            <button type="button" className="btn btn-link text-white p-0"><i className="fas fa-play-circle fa-2x"></i></button>
          </div>
          <p className="small text-white-50 mt-3">%s</p>
        </div>
      </div>
      <hr className="border-light" />
      <div className="text-center small">&copy; {new Date().getFullYear()} <strong>{SITE_NAME}</strong> %s</div>
    </div>
    <style>{`.footer-gradient{background:linear-gradient(135deg,rgb(9,17,65),rgb(8,17,60));}`}</style>
  </footer>
);
export default Footer;
''' % (
        '\u8054\u7cfb\u6211\u4eec',
        '\u56db\u5ddd\u7701\u6210\u90fd\u5e02\u9ad8\u65b0\u533a\u6696\u722a\u8def 88 \u53f7',
        '\u5feb\u6377\u5165\u53e3',
        '\u9886\u517b\u5ba0\u7269', '\u79d1\u666e\u4e0e\u516c\u544a', '\u62a5\u5931\u5bfb\u4e3b', '\u4e92\u52a8\u793e\u533a',
        '\u5173\u6ce8\u6211\u4eec',
        '\u793e\u4ea4\u5e73\u53f0\u94fe\u63a5\u4ec5\u4e3a\u5c55\u793a\uff0c\u6682\u672a\u5f00\u653e\u8df3\u8f6c',
        '\u00b7 \u4fdd\u7559\u6240\u6709\u6743\u5229',
    )
    w('src/components/Footer.js', footer)

    navbar = '''import { useCallback, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../api/api';
import { SITE_NAME } from '../constants/site';

const Navbar = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const token = localStorage.getItem('token');

  const fetchUserProfile = useCallback(async () => {
    try {
      const res = await authAPI.getProfile();
      setUser(res.data);
      setIsAdmin(res.data.profile?.role === 'admin');
    } catch {
      localStorage.removeItem('token');
      navigate('/login');
    }
  }, [navigate]);

  useEffect(() => { if (token) fetchUserProfile(); }, [token, fetchUserProfile]);

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setIsAdmin(false);
    navigate('/');
  };

  const L = {
    home: '%s', pets: '%s', cms: '%s', lost: '%s', comm: '%s', rescue: '%s',
    add: '%s', dash: '%s', admin: '%s', profile: '%s', my: '%s', out: '%s', login: '%s', reg: '%s', user: '%s',
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark" style={{backgroundColor:'#ff8c00'}}>
      <div className="container">
        <Link className="navbar-brand fw-bold" to="/"><i className="fas fa-paw me-2"></i>{SITE_NAME}</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"><span className="navbar-toggler-icon"></span></button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto">
            <li className="nav-item"><Link className="nav-link" to="/">{L.home}</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/pets">{L.pets}</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/cms">{L.cms}</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/lost-found">{L.lost}</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/community">{L.comm}</Link></li>
            <li className="nav-item"><Link className="nav-link" to="/rescue">{L.rescue}</Link></li>
            {token && isAdmin && <li className="nav-item"><Link className="nav-link" to="/add-pet">{L.add}</Link></li>}
            {token && <li className="nav-item"><Link className="nav-link" to="/dashboard">{L.dash}</Link></li>}
            {token && isAdmin && <li className="nav-item"><Link className="nav-link" to="/admin">{L.admin}</Link></li>}
          </ul>
          <ul className="navbar-nav">
            {token ? (
              <li className="nav-item dropdown">
                <button className="nav-link dropdown-toggle btn" data-bs-toggle="dropdown" style={{background:'transparent',border:'none',color:'inherit'}}>
                  {user?.profile?.nickname || user?.username || L.user}
                </button>
                <ul className="dropdown-menu dropdown-menu-end">
                  <li><Link className="dropdown-item" to="/profile">{L.profile}</Link></li>
                  <li><Link className="dropdown-item" to="/my-pets">{L.my}</Link></li>
                  <li><hr className="dropdown-divider"/></li>
                  <li><button type="button" className="dropdown-item" onClick={logout}>{L.out}</button></li>
                </ul>
              </li>
            ) : (
              <>
                <li className="nav-item"><Link className="nav-link" to="/login">{L.login}</Link></li>
                <li className="nav-item"><Link className="nav-link" to="/register">{L.reg}</Link></li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};
export default Navbar;
''' % (
        '\u9996\u9875', '\u9886\u517b\u5ba0\u7269', '\u79d1\u666e\u516c\u544a', '\u62a5\u5931\u5bfb\u4e3b',
        '\u793e\u533a', '\u6551\u52a9\u8ffd\u8e2a', '\u6dfb\u52a0\u6863\u6848', '\u6211\u7684\u9886\u517b', '\u7ba1\u7406\u540e\u53f0',
        '\u4e2a\u4eba\u4e2d\u5fc3', '\u6211\u7684\u6551\u52a9', '\u9000\u51fa\u767b\u5f55', '\u767b\u5f55', '\u6ce8\u518c', '\u7528\u6237',
    )
    w('src/components/Navbar.js', navbar)


if __name__ == '__main__':
    main()
