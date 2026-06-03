import React, { useEffect, useRef, useState } from 'react';
import { aiAPI } from '../api/api';
import './AiAssistantWidget.css';

const DRAG_THRESHOLD_PX = 8;

const AiAssistantWidget = () => {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: 'assistant', content: '你好，我是暖爪智能养宠助手，有什么养宠问题可以问我。' },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [pos, setPos] = useState({ x: null, y: null });
  const [pointerActive, setPointerActive] = useState(false);
  const rootRef = useRef(null);
  const dragOffsetRef = useRef({ offsetX: 0, offsetY: 0 });
  const pointerStartRef = useRef({ x: 0, y: 0 });
  const dragModeRef = useRef('fab');
  const movedRef = useRef(false);

  useEffect(() => {
    const saved = localStorage.getItem('aiWidgetPos');
    if (saved) {
      try {
        setPos(JSON.parse(saved));
      } catch {
        /* ignore */
      }
    }
  }, []);

  const savePosition = (x, y) => {
    const next = { x, y };
    setPos(next);
    localStorage.setItem('aiWidgetPos', JSON.stringify(next));
  };

  const beginPointerDrag = (e, mode) => {
    if (!rootRef.current) return;
    const rect = rootRef.current.getBoundingClientRect();
    dragOffsetRef.current = {
      offsetX: e.clientX - rect.left,
      offsetY: e.clientY - rect.top,
    };
    pointerStartRef.current = { x: e.clientX, y: e.clientY };
    dragModeRef.current = mode;
    movedRef.current = mode === 'handle';
    setPointerActive(true);
    if (mode === 'handle') {
      document.body.classList.add('ai-widget-dragging');
    }
  };

  useEffect(() => {
    if (!pointerActive) return undefined;

    const onMove = (e) => {
      if (!movedRef.current && dragModeRef.current === 'fab') {
        const dx = e.clientX - pointerStartRef.current.x;
        const dy = e.clientY - pointerStartRef.current.y;
        if (dx * dx + dy * dy < DRAG_THRESHOLD_PX * DRAG_THRESHOLD_PX) {
          return;
        }
        movedRef.current = true;
        document.body.classList.add('ai-widget-dragging');
      }
      if (!movedRef.current) return;
      setPos({
        x: e.clientX - dragOffsetRef.current.offsetX,
        y: e.clientY - dragOffsetRef.current.offsetY,
      });
    };

    const onUp = (e) => {
      if (movedRef.current) {
        savePosition(
          e.clientX - dragOffsetRef.current.offsetX,
          e.clientY - dragOffsetRef.current.offsetY,
        );
      } else if (dragModeRef.current === 'fab') {
        setOpen((o) => !o);
      }
      movedRef.current = false;
      setPointerActive(false);
      document.body.classList.remove('ai-widget-dragging');
    };

    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);
    window.addEventListener('pointercancel', onUp);
    return () => {
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      window.removeEventListener('pointercancel', onUp);
      document.body.classList.remove('ai-widget-dragging');
    };
  }, [pointerActive]);

  const onDragHandleDown = (e) => {
    e.preventDefault();
    e.stopPropagation();
    beginPointerDrag(e, 'handle');
  };

  const onFabPointerDown = (e) => {
    e.preventDefault();
    beginPointerDrag(e, 'fab');
    e.currentTarget.setPointerCapture(e.pointerId);
  };

  const send = async () => {
    const q = input.trim();
    if (!q || loading) return;
    if (!localStorage.getItem('token')) {
      alert('请先登录后使用智能助手');
      return;
    }
    const nextMsgs = [...messages, { role: 'user', content: q }];
    setMessages(nextMsgs);
    setInput('');
    setLoading(true);
    try {
      const history = nextMsgs.slice(-8);
      const res = await aiAPI.qa({ question: q, history });
      setMessages((m) => [...m, { role: 'assistant', content: res.data.answer }]);
    } catch (err) {
      let detail = err.response?.data?.detail || '';
      if (err.code === 'ECONNABORTED') {
        detail = '请求超时，请稍后重试';
      } else if (!detail) {
        detail = '请求失败，请确认后端已启动且 LLM 已配置';
      }
      setMessages((m) => [...m, { role: 'assistant', content: detail }]);
    } finally {
      setLoading(false);
    }
  };

  const style = pos.x != null ? { left: pos.x, top: pos.y, right: 'auto', bottom: 'auto' } : {};
  const fabDragging = pointerActive && movedRef.current;

  return (
    <div className="ai-widget-root" style={style} ref={rootRef}>
      {open && (
        <div className="ai-panel card shadow">
          <div className="card-header d-flex justify-content-between align-items-center py-2 gap-2">
            <button
              type="button"
              className="ai-drag-handle btn btn-sm btn-light border"
              title="拖动位置"
              aria-label="拖动助手位置"
              onPointerDown={onDragHandleDown}
            >
              <i className="fas fa-grip-lines" />
            </button>
            <span className="fw-semibold small flex-grow-1 text-center">智能养宠助手</span>
            <button type="button" className="btn-close btn-sm" aria-label="关闭" onClick={() => setOpen(false)} />
          </div>
          <div className="ai-disclaimer" role="note">
            <i className="fas fa-exclamation-triangle text-warning" aria-hidden />
            <span>
              AI 回答仅供参考，不能替代兽医诊断；宠物不适或生病请尽快就医。
            </span>
          </div>
          <div className="ai-panel-messages">
            {messages.map((m, i) => (
              <div key={i} className={`ai-msg ai-msg-${m.role}`}>{m.content}</div>
            ))}
            {loading && <div className="text-muted small">思考中...</div>}
          </div>
          <div className="card-footer p-2">
            <div className="input-group input-group-sm">
              <input
                className="form-control ai-panel-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && send()}
                placeholder="输入养宠问题..."
              />
              <button type="button" className="btn btn-success" onClick={send} disabled={loading}>发送</button>
            </div>
          </div>
        </div>
      )}
      <button
        type="button"
        className={`ai-fab btn btn-success rounded-circle shadow${fabDragging ? ' ai-fab-dragging' : ''}`}
        onPointerDown={onFabPointerDown}
        title="智能养宠助手（拖动可移动位置，点击打开）"
        aria-expanded={open}
      >
        <i className="fas fa-robot" />
      </button>
    </div>
  );
};

export default AiAssistantWidget;
