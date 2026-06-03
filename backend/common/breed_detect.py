import json
import time

from common.breed_classifier import BreedModelNotReadyError, is_model_ready, model_paths, predict_breeds
from common.image_loader import load_image_for_ai

_LOW_CONFIDENCE_THRESHOLD = 0.35
_UNCERTAIN = '\u4e0d\u786e\u5b9a'
_NONE = '\u65e0'


def _fallback_breeds_for_species(species: str) -> list[dict]:
    s = (species or '').strip()
    if '\u732b' in s:
        return [
            {'breed': '\u4e2d\u534e\u7530\u56ed\u732b', 'confidence': 0.45},
            {'breed': '\u6df7\u8840\u4e2a\u4f53\uff08\u54c1\u79cd\u5f85\u786e\u8ba4\uff09', 'confidence': 0.35},
        ]
    if '\u72d7' in s:
        return [
            {'breed': '\u4e2d\u534e\u7530\u56ed\u72ac', 'confidence': 0.45},
            {'breed': '\u6df7\u8840\u4e2a\u4f53\uff08\u54c1\u79cd\u5f85\u786e\u8ba4\uff09', 'confidence': 0.35},
        ]
    return [
        {'breed': '\u6df7\u8840\u4e2a\u4f53\uff08\u54c1\u79cd\u5f85\u786e\u8ba4\uff09', 'confidence': 0.45},
        {'breed': '\u54c1\u79cd\u5f85\u8fdb\u4e00\u6b65\u786e\u8ba4', 'confidence': 0.35},
    ]


def _ensure_breed_candidates(species: str, candidates: list[dict]) -> tuple[list[dict], bool]:
    fallbacks = _fallback_breeds_for_species(species)
    if not candidates:
        return fallbacks[:2], True

    max_conf = max(c['confidence'] for c in candidates)
    if max_conf >= _LOW_CONFIDENCE_THRESHOLD:
        return candidates[:4], False

    primary = fallbacks[0]
    merged = [primary]
    for item in candidates:
        if item['breed'] != primary['breed']:
            merged.append(item)
    if len(merged) < 2 and len(fallbacks) > 1:
        secondary = fallbacks[1]
        if secondary['breed'] not in {m['breed'] for m in merged}:
            merged.append(secondary)
    return merged[:4], True


def _build_result_text(species: str, candidates: list[dict]) -> str:
    if not candidates:
        return f'\u7269\u79cd\uff1a{species}' if species else ''
    top = candidates[0]
    pct = int(top['confidence'] * 100)
    return f"\u63a8\u8350\u54c1\u79cd\uff1a{top['breed']}\uff08\u7f6e\u4fe1\u5ea6\u7ea6 {pct}%\uff09"


def _predictions_to_payload(predictions: list[dict]) -> dict:
    if not predictions:
        species = _UNCERTAIN
        candidates, low_confidence = _ensure_breed_candidates(species, [])
    else:
        species_counts = {}
        for item in predictions:
            species_counts[item['species']] = species_counts.get(item['species'], 0) + item['confidence']
        species = max(species_counts, key=species_counts.get) if species_counts else _UNCERTAIN

        seen = set()
        candidates = []
        for item in predictions:
            key = item['breed']
            if key in seen:
                continue
            seen.add(key)
            candidates.append({'breed': item['breed'], 'confidence': item['confidence']})
        candidates, low_confidence = _ensure_breed_candidates(species, candidates)

    breed = candidates[0]['breed'] if candidates else _UNCERTAIN
    result_text = _build_result_text(species, candidates)

    return {
        'species': species,
        'breed': breed,
        'summary': '',
        'result': result_text,
        'breed_candidates': candidates,
        'low_confidence': low_confidence,
        'confidence': candidates[0]['confidence'] if candidates else 0.0,
    }


def detect_pet_breed(*, image_url: str = '', image_base64: str = '', description: str = '', request=None) -> dict:
    if not is_model_ready():
        paths = model_paths()
        raise BreedModelNotReadyError(
            f'\u672c\u5730\u54c1\u79cd\u6a21\u578b\u672a\u5c31\u7eea\u3002\u8bf7\u5728\u9879\u76ee\u6839\u76ee\u5f55\u6267\u884c\uff1a'
            f'backend\\venv\\Scripts\\python.exe scripts\\download_breed_model.py'
            f'\uff08\u6216 scripts\\train_breed_model.py\uff09\u3002\u6743\u91cd\u8def\u5f84\uff1a{paths["weights"]}'
        )

    image = load_image_for_ai(
        image_url=image_url,
        image_base64=image_base64,
        request=request,
    )

    started = time.perf_counter()
    predictions, infer_ms = predict_breeds(image['bytes'], top_k=4)
    formatted = _predictions_to_payload(predictions)

    return {
        'result': formatted['result'],
        'breed': formatted['breed'],
        'species': formatted['species'],
        'summary': formatted['summary'],
        'breed_candidates': formatted['breed_candidates'],
        'low_confidence': formatted['low_confidence'],
        'confidence': formatted['confidence'],
        'vision_used': False,
        'model_source': 'local_cnn',
        'object_recognition': False,
        'object_labels': [],
        'object_error': '',
        'debug_meta': json.dumps({
            'filename': image['filename'],
            'bytes': len(image['bytes']),
            'infer_ms': infer_ms,
            'total_ms': int((time.perf_counter() - started) * 1000),
            'description': (description or '')[:80],
        }, ensure_ascii=False),
    }
