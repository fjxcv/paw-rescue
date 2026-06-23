# -*- coding: utf-8 -*-
"""Apply UTF-8-safe patches to LostFoundPublish.js (ASCII source only)."""
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'frontend' / 'src' / 'pages' / 'LostFoundPublish.js'
text = path.read_text(encoding='utf-8')

text = text.replace(
    "import { formatApiError, roundCoordinate } from '../utils/apiError';\n\n"
    "// ============================================================\n"
    "// \u9ad8\u5fb7\u5730\u56fe Web API \u914d\u7f6e\n"
    "// \u4f7f\u7528\u524d\u8bf7\u5c06\u4e0b\u65b9\u5360\u4f4d\u7b26\u66ff\u6362\u4e3a\u4f60\u81ea\u5df1\u7684\u9ad8\u5fb7 Web API Key\n"
    "// \u7533\u8bf7\u5730\u5740\uff1ahttps://console.amap.com/dev/key/app\n"
    "// ============================================================\n"
    "const AMAP_KEY = 'e9b57a099f261b32a70742305ae7e705'; // \u2190 \u8bf7\u66ff\u6362\u4e3a\u4f60\u7684\u9ad8\u5fb7 Key\n",
    "import { AMAP_KEY, AMAP_TILE_URL, AMAP_TILE_OPTIONS } from '../config/amap';\n"
    "import { formatApiError, roundCoordinate } from '../utils/apiError';\n",
)

text = text.replace(
    "    // \u9ad8\u5fb7\u5750\u6807\uff08GCJ-02\uff09\u8f6c WGS-84 \u7528\u4e8e Leaflet \u5730\u56fe\n"
    "    const wgs = gcj02ToWgs84(gcjLat, gcjLng);\n"
    "    return {\n"
    "      id: poi.id,\n"
    "      name: poi.name,\n"
    "      address: poi.address || '',\n"
    "      lat: wgs.lat,\n"
    "      lng: wgs.lng,\n",
    "    return {\n"
    "      id: poi.id,\n"
    "      name: poi.name,\n"
    "      address: poi.address || '',\n"
    "      lat: gcjLat,\n"
    "      lng: gcjLng,\n",
)

text = text.replace(
    "      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {\n"
    "        maxZoom: 19,\n"
    "        attribution: '&copy; OpenStreetMap',\n"
    "      }).addTo(map);",
    "      L.tileLayer(AMAP_TILE_URL, AMAP_TILE_OPTIONS).addTo(map);",
)

text = text.replace(
    "    return () => { cancelled = true; };",
    "    return () => {\n"
    "      cancelled = true;\n"
    "      if (leafletMapRef.current) {\n"
    "        leafletMapRef.current.remove();\n"
    "        leafletMapRef.current = null;\n"
    "        markerRef.current = null;\n"
    "        setMapReady(false);\n"
    "      }\n"
    "    };",
)

text = text.replace(
    "      return;\n"
    "    }\n"
    "    setSubmitting(true);\n"
    "    setError('');\n"
    "    try {",
    "      return;\n"
    "    }\n"
    "    if (!photoUrls.length) {\n"
    "      setError('\u8bf7\u81f3\u5c11\u4e0a\u4f20 1 \u5f20\u5ba0\u7269\u7167\u7247\u3002');\n"
    "      return;\n"
    "    }\n"
    "    setSubmitting(true);\n"
    "    setError('');\n"
    "    try {",
)

post_type_old = (
    "            <div className=\"col-md-6\">\n"
    "              <label className=\"form-label\">\u7c7b\u578b</label>\n"
    "              <select name=\"post_type\" className=\"form-select\" value={form.post_type} onChange={handleChange} required>\n"
    "                <option value=\"lost\">{LOST_FOUND_TYPE.lost}\uff08\u4e22\u5931\uff09</option>\n"
    "                <option value=\"found\">{LOST_FOUND_TYPE.found}\uff08\u53d1\u73b0\uff09</option>\n"
    "              </select>\n"
    "            </div>\n"
    "            <div className=\"col-md-6\">"
)
post_type_new = (
    "            <div className=\"col-12\">\n"
    "              <label className=\"form-label d-block\">\u7c7b\u578b <span className=\"text-danger\">*</span></label>\n"
    "              <div className=\"btn-group w-100 flex-wrap\" role=\"group\">\n"
    "                {Object.entries(LOST_FOUND_TYPE).map(([key, label]) => (\n"
    "                  <button\n"
    "                    key={key}\n"
    "                    type=\"button\"\n"
    "                    className={`btn flex-fill ${form.post_type === key ? 'btn-success' : 'btn-outline-secondary'}`}\n"
    "                    onClick={() => setForm((f) => ({ ...f, post_type: key }))}\n"
    "                  >\n"
    "                    {label}\n"
    "                    <small className=\"d-block opacity-75\">{key === 'lost' ? '\u5ba0\u7269\u8d70\u5931' : '\u53d1\u73b0\u6d41\u6d6a/\u62db\u9886'}</small>\n"
    "                  </button>\n"
    "                ))}\n"
    "              </div>\n"
    "            </div>\n"
    "            <div className=\"col-md-6\">"
)
if post_type_old not in text:
    raise SystemExit('post_type block not found')
text = text.replace(post_type_old, post_type_new)

path.write_text(text, encoding='utf-8', newline='\n')
print('patched', path)
