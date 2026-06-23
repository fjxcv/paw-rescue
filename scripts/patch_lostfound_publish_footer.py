# -*- coding: utf-8 -*-
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'frontend/src/pages/LostFoundPublish.js'
text = path.read_text(encoding='utf-8')

if 'photoError' not in text:
    text = text.replace(
        "  const [error, setError] = useState('');\n",
        "  const [error, setError] = useState('');\n  const [photoError, setPhotoError] = useState('');\n",
    )
    text = text.replace(
        "    if (!photoUrls.length) {\n      setError('\u8bf7\u81f3\u5c11\u4e0a\u4f20 1 \u5f20\u5ba0\u7269\u7167\u7247\u3002');\n      return;\n    }\n",
        "    if (!photoUrls.length) {\n      setPhotoError('\u8bf7\u81f3\u5c11\u4e0a\u4f20 1 \u5f20\u5ba0\u7269\u7167\u7247\u3002');\n      return;\n    }\n    setPhotoError('');\n",
    )
    text = text.replace(
        "              <label className=\"form-label\">\u7167\u7247</label>\n",
        "              <label className=\"form-label\">\u7167\u7247 <span className=\"text-danger\">*</span> <small className=\"text-muted\">(\u81f3\u5c11 1 \u5f20)</small></label>\n",
    )
    text = text.replace(
        "        <div className=\"card-footer d-flex gap-2\">\n          <button type=\"submit\"",
        "        <div className=\"card-footer\">\n          {photoError && <div className=\"alert alert-danger py-2 mb-2\">{photoError}</div>}\n          <div className=\"d-flex gap-2\">\n          <button type=\"submit\"",
    )
    text = text.replace(
        "          <Link to=\"/lost-found\" className=\"btn btn-outline-secondary\">\u53d6\u6d88</Link>\n        </div>\n      </form>",
        "          <Link to=\"/lost-found\" className=\"btn btn-outline-secondary\">\u53d6\u6d88</Link>\n          </div>\n        </div>\n      </form>",
    )
    # fallback if labels differ
    if 'photoError' not in text:
        raise SystemExit('photo patch partial fail')

path.write_text(text, encoding='utf-8', newline='\n')
print('lostfound publish patched')
