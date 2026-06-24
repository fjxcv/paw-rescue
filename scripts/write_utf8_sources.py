# -*- coding: utf-8 -*-
"""Rewrite key UTF-8 sources that may display as mojibake."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def write_index_html():
    content = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="description" content="\u6696\u722a\u6551\u52a9 - \u6d41\u6d6a\u5ba0\u7269\u7efc\u5408\u6551\u52a9\u7ba1\u7406\u5e73\u53f0" />
<title>\u6696\u722a\u6551\u52a9</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" crossorigin="anonymous" />
</head>
<body><noscript>\u8bf7\u542f\u7528 JavaScript\u3002</noscript><div id="root"></div></body></html>
'''
    (ROOT / 'frontend/public/index.html').write_text(content, encoding='utf-8', newline='\n')


def write_site_js():
    content = '''export const SITE_NAME = '\u6696\u722a\u6551\u52a9';

export const ADOPTION_STATUS = {available:'\u53ef\u9886\u517b',pending:'\u7533\u8bf7\u4e2d',adopted:'\u5df2\u9886\u517b'};
export const ONLINE_STATUS = {pending:'\u5f85\u5ba1\u6838',approved:'\u5df2\u901a\u8fc7',rejected:'\u5df2\u62d2\u7edd',need_material:'\u9700\u8865\u6750\u6599'};
export const ARTICLE_TYPES = {science:'\u79d1\u666e',announcement:'\u516c\u544a',law:'\u6cd5\u89c4',rescue_case:'\u6551\u52a9\u6848\u4f8b'};
export const POST_CATEGORIES = {general:'\u7efc\u5408',rescue_share:'\u6551\u52a9\u5206\u4eab',help_request:'\u6c42\u52a9',pet_experience:'\u517b\u5ba0\u7ecf\u9a8c'};
export const LOST_FOUND_TYPE = {lost:'\u5bfb\u5ba0',found:'\u62db\u9886'};
export const LOST_FOUND_STATUS = {searching:'\u5bfb\u627e\u4e2d',found:'\u5df2\u627e\u5230',cancelled:'\u5df2\u53d6\u6d88'};
export const RESCUE_STATUS = {pending_rescue:'\u5f85\u6551\u52a9',in_medical:'\u533b\u7597\u4e2d',recovering:'\u6062\u590d\u4e2d',awaiting_adoption:'\u5f85\u9886\u517b',rescued:'\u6551\u52a9\u6210\u529f',abandoned:'\u5df2\u7ec8\u6b62'};
export const SIZE_CATEGORY = {small:'\u5c0f\u578b',medium:'\u4e2d\u578b',large:'\u5927\u578b'};
export const HEALTH_STATUS = {healthy:'\u5065\u5eb7',minor_injury:'\u8f7b\u5fae\u4f24\u75c5',severe_injury:'\u4e25\u91cd\u4f24\u75c5'};
'''
    (ROOT / 'frontend/src/constants/site.js').write_text(content, encoding='utf-8', newline='\n')


def fix_navbar():
    path = ROOT / 'frontend/src/components/Navbar.js'
    t = path.read_text(encoding='utf-8')
    old_start = '  const L = {'
    old_end = '  };'
    si = t.find(old_start)
    ei = t.find(old_end, si) + len(old_end)
    new_l = """  const L = {
    home: '\u9996\u9875', pets: '\u9886\u517b\u5ba0\u7269', cms: '\u79d1\u666e\u516c\u544a', lost: '\u62a5\u5931\u5bfb\u4e3b', comm: '\u793e\u533a', rescue: '\u6551\u52a9\u8ddf\u8e2a',
    add: '\u6dfb\u52a0\u6863\u6848', dash: '\u6211\u7684\u9886\u517b', admin: '\u7ba1\u7406\u540e\u53f0', profile: '\u4e2a\u4eba\u4e2d\u5fc3', publicPage: '\u6211\u7684\u4e3b\u9875', editProfile: '\u7f16\u8f91\u8d44\u6599', my: '\u6211\u7684\u6551\u52a9', out: '\u9000\u51fa\u767b\u5f55', login: '\u767b\u5f55', reg: '\u6ce8\u518c', user: '\u7528\u6237', manage: '\u7ba1\u7406\u6a21\u5f0f',
  };"""
    if si == -1:
        raise SystemExit('Navbar L block not found')
    t = t[:si] + new_l + t[ei:]
    t = t.replace('aria-label="\u9422\u5a41\u57ab\u9451\u5d41\u5d17"', 'aria-label="\u7528\u6237\u83dc\u5355"')
    t = t.replace('aria-label="', 'aria-label="', 1)  # noop
    import re
    t = re.sub(r'aria-label="[^"]*"', 'aria-label="\u7528\u6237\u83dc\u5355"', t, count=1)
    path.write_text(t, encoding='utf-8', newline='\n')


def fix_portal_models():
    path = ROOT / 'backend/portal/models.py'
    lines = path.read_text(encoding='utf-8').splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith('"""') and i < 8:
            lines[i] = '    """\u9996\u9875\u8f6e\u64ad\u56fe"""'
            break
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def fix_utf8_rule():
    path = ROOT.parent / '.cursor/rules/utf8-encoding.mdc'
    if not path.exists():
        return
    text = (
        '---\n'
        'description: Prevent Chinese mojibake - all source must be UTF-8 on disk\n'
        'globs:\n'
        '  - paw-rescue/**/*\n'
        'alwaysApply: false\n'
        '---\n\n'
        '# UTF-8 \u7f16\u7801\uff08\u4e2d\u6587\u754c\u9762\u5fc5\u5b88\uff09\n\n'
        'Windows \u4e0b\u8bf7\u786e\u4fdd\u6240\u6709\u542b\u4e2d\u6587\u7684\u6e90\u7801\u4ee5 **UTF-8\uff08\u65e0 BOM\uff09** \u4fdd\u5b58\u3002\n\n'
        '\u4fee\u6539\u540e\u6267\u884c\uff1a`python scripts/ensure_utf8.py --check`\n'
    )
    path.write_text(text, encoding='utf-8', newline='\n')


if __name__ == '__main__':
    write_index_html()
    write_site_js()
    fix_navbar()
    fix_portal_models()
    fix_utf8_rule()
    print('UTF-8 sources rewritten')
