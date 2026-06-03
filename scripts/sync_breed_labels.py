#!/usr/bin/env python
"""Write backend/ml/breed_labels.json in Oxford-IIIT Pet label-id order."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / 'backend'
sys.path.insert(0, str(BACKEND))

from torchvision import datasets  # noqa: E402

ML_DIR = BACKEND / 'ml'
LABELS_PATH = ML_DIR / 'breed_labels.json'

_CAT = '\u732b'
_DOG = '\u72d7'

# Display names from torchvision OxfordIIITPet.classes
ZH_BY_CLASS = {
    'Abyssinian': ('\u963f\u6bd4\u897f\u5c3c\u4e9a\u732b', _CAT),
    'American Bulldog': ('\u7f8e\u56fd\u6597\u725b\u72ac', _DOG),
    'American Pit Bull Terrier': ('\u7f8e\u56fd\u6bd4\u7279\u72ac', _DOG),
    'Basset Hound': ('\u5df4\u5409\u5ea6\u730e\u72ac', _DOG),
    'Beagle': ('\u6bd4\u683c\u72ac', _DOG),
    'Bengal': ('\u5b5f\u52a0\u62c9\u732b', _CAT),
    'Birman': ('\u4f2f\u66fc\u732b', _CAT),
    'Bombay': ('\u5b5f\u4e70\u732b', _CAT),
    'Boxer': ('\u62f3\u5e08\u72ac', _DOG),
    'British Shorthair': ('\u82f1\u56fd\u77ed\u6bdb\u732b', _CAT),
    'Burmese': ('\u7f05\u7538\u732b', _CAT),
    'Chihuahua': ('\u5409\u5a03\u5a03', _DOG),
    'Egyptian Mau': ('\u57c3\u53ca\u732b', _CAT),
    'English Cocker Spaniel': ('\u82f1\u56fd\u53ef\u5361\u72ac', _DOG),
    'English Setter': ('\u82f1\u56fd\u585e\u7279\u72ac', _DOG),
    'German Shorthaired': ('\u5fb7\u56fd\u77ed\u6bdb\u6307\u793a\u72ac', _DOG),
    'Great Pyrenees': ('\u5927\u767d\u718a\u72ac', _DOG),
    'Havanese': ('\u54c8\u74e6\u90a3\u72ac', _DOG),
    'Japanese Chin': ('\u65e5\u672c\u72b6', _DOG),
    'Keeshond': ('\u8377\u5170\u6bdb\u72ee\u72ac', _DOG),
    'Leonberger': ('\u83b1\u6602\u8d1d\u683c\u72ac', _DOG),
    'Maine Coon': ('\u7f05\u56e0\u732b', _CAT),
    'Miniature Pinscher': ('\u8ff7\u4f60\u675c\u5bbe\u72ac', _DOG),
    'Newfoundland': ('\u7ebd\u82ac\u5170\u72ac', _DOG),
    'Persian': ('\u6ce2\u65af\u732b', _CAT),
    'Pomeranian': ('\u535a\u7f8e\u72ac', _DOG),
    'Pug': ('\u5df4\u54e5\u72ac', _DOG),
    'Ragdoll': ('\u5e03\u5076\u732b', _CAT),
    'Russian Blue': ('\u4fc4\u7f57\u65af\u84dd\u732b', _CAT),
    'Saint Bernard': ('\u5723\u4f2f\u7eb3\u72ac', _DOG),
    'Samoyed': ('\u6492\u6469\u8036', _DOG),
    'Scottish Terrier': ('\u82cf\u683c\u5170\u6897', _DOG),
    'Shiba Inu': ('\u67f4\u72ac', _DOG),
    'Siamese': ('\u66d9\u7f57\u732b', _CAT),
    'Sphynx': ('\u65af\u82ac\u514b\u65af\u732b', _CAT),
    'Staffordshire Bull Terrier': ('\u65af\u5854\u798f\u90e1\u6597\u725b\u6897', _DOG),
    'Wheaten Terrier': ('\u8f6f\u6bdb\u5c0f\u9ea6\u6897', _DOG),
    'Yorkshire Terrier': ('\u7ea6\u514b\u590f\u6897', _DOG),
}


def build_labels(class_names: list[str]) -> list[dict]:
    labels = []
    for name in class_names:
        zh, species = ZH_BY_CLASS.get(name, (name, _DOG))
        labels.append({'en': name, 'zh': zh, 'species': species})
    return labels


def main(download: bool = False) -> int:
    dataset = datasets.OxfordIIITPet(
        root=str(ML_DIR / 'data'),
        download=download,
        target_types='category',
    )
    labels = build_labels(list(dataset.classes))
    ML_DIR.mkdir(parents=True, exist_ok=True)
    with open(LABELS_PATH, 'w', encoding='utf-8') as f:
        json.dump(labels, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'Wrote {len(labels)} labels to {LABELS_PATH}')
    for i, item in enumerate(labels):
        print(f'{i:02d} {item["en"]} -> {item["zh"]} ({item["species"]})')
    return 0


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args()
    raise SystemExit(main(download=args.download))
