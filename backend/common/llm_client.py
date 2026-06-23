import json
import os
import urllib.error
import urllib.request


class LLMNotConfiguredError(Exception):
    pass


class LLMRequestError(Exception):
    pass


def _chat_completion(messages, max_tokens=1024):
    api_key = os.getenv('LLM_API_KEY', '').strip()
    if not api_key:
        raise LLMNotConfiguredError(
            '\u672a\u914d\u7f6e LLM_API_KEY\uff0c\u8bf7\u5728 backend/.env \u4e2d\u8bbe\u7f6e\u540e\u91cd\u542f\u540e\u7aef\u3002'
        )
    base = os.getenv('LLM_API_BASE', 'https://api.openai.com/v1').rstrip('/')
    model = os.getenv('LLM_MODEL', 'gpt-4o-mini')
    url = f'{base}/chat/completions'
    payload = json.dumps({
        'model': model,
        'messages': messages,
        'max_tokens': max_tokens,
        'temperature': 0.7,
    }).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode('utf-8', errors='replace')
        raise LLMRequestError(f'LLM HTTP {exc.code}: {err_body[:500]}') from exc
    except urllib.error.URLError as exc:
        raise LLMRequestError(f'LLM connection error: {exc}') from exc
    choices = body.get('choices') or []
    if not choices:
        raise LLMRequestError('LLM returned empty choices')
    content = choices[0].get('message', {}).get('content', '')
    return (content or '').strip()


def chat(messages, max_tokens=1024):
    return _chat_completion(messages, max_tokens=max_tokens)


def chat_vision(image_data_url: str, user_text: str, system_prompt: str, max_tokens=512):
    messages = [
        {'role': 'system', 'content': system_prompt},
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': user_text},
                {'type': 'image_url', 'image_url': {'url': image_data_url}},
            ],
        },
    ]
    return _chat_completion(messages, max_tokens=max_tokens)
