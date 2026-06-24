import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

export default function RegisterForm() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [password, setPassword] = useState('');
  const [sending, setSending] = useState(false);
  const [count, setCount] = useState(0);
  const timerRef = useRef(null);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    if (count <= 0) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, [count]);

  useEffect(() => {
    return () => clearInterval(timerRef.current);
  }, []);

  const startCountdown = (seconds = 60) => {
    setCount(seconds);
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setCount(prev => {
        if (prev <= 1) {
          clearInterval(timerRef.current);
          timerRef.current = null;
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  const requestCode = async () => {
    setMessage(null);
    if (!email) {
      setMessage({ type: 'error', text: '请输入邮箱地址' });
      return;
    }
    setSending(true);
    try {
      await axios.post('/api/auth/email/register-request/', { email });
      setMessage({ type: 'success', text: '验证码已发送，请查看邮箱（含垃圾箱）' });
      startCountdown(60);
    } catch (err) {
      const text = err?.response?.data?.detail || err.message || '发送失败';
      setMessage({ type: 'error', text });
    } finally {
      setSending(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);
    try {
      const payload = {
        username,
        email,
        password,
        code,
        has_privacy_consent: true,
      };
      const resp = await axios.post('/api/register/', payload);
      setMessage({ type: 'success', text: '注册成功' });
      // optionally redirect or clear form
    } catch (err) {
      const detail = err?.response?.data || err.message;
      // show first error message if available
      let text = '注册失败';
      if (detail && typeof detail === 'object') {
        if (detail.detail) text = detail.detail;
        else {
          const vals = Object.values(detail);
          if (vals.length) text = Array.isArray(vals[0]) ? vals[0][0] : String(vals[0]);
        }
      } else if (typeof detail === 'string') text = detail;
      setMessage({ type: 'error', text });
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 520, margin: '0 auto' }}>
      <div style={{ marginBottom: 12 }}>
        <label>用户名</label>
        <input
          className="form-control"
          value={username}
          onChange={e => setUsername(e.target.value)}
          required
        />
      </div>

      <div style={{ marginBottom: 12 }}>
        <label>邮箱</label>
        <input
          className="form-control"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
        <div style={{ flex: 1 }}>
          <label>验证码</label>
          <input
            className="form-control"
            value={code}
            onChange={e => setCode(e.target.value)}
            required
          />
        </div>
        <div style={{ width: 140, marginTop: 22 }}>
          <button
            type="button"
            className="btn btn-primary"
            onClick={requestCode}
            disabled={sending || count > 0}
            style={{ width: '100%' }}
          >
            {count > 0 ? `${count}s` : '获取验证码'}
          </button>
        </div>
      </div>

      <div style={{ marginBottom: 12 }}>
        <label>密码</label>
        <input
          className="form-control"
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
      </div>

      <div style={{ marginTop: 16 }}>
        <button className="btn btn-success" type="submit" style={{ width: '100%' }}>
          注册
        </button>
      </div>

      {message && (
        <div style={{ marginTop: 12 }}>
          <div className={message.type === 'error' ? 'alert alert-danger' : 'alert alert-success'}>
            {message.text}
          </div>
        </div>
      )}
    </form>
  );
}
