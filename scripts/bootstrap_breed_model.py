#!/usr/bin/env python
"""
Fast bootstrap: download Oxford annotations only, sync labels, save ImageNet-backed weights.
Full fine-tune later: scripts/train_breed_model.py
"""
from __future__ import annotations

import json
import sys
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'
BACKEND = ROOT / 'backend'
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(SCRIPTS))

import torch
import torch.nn as nn
from torchvision import models

from sync_breed_labels import build_labels

ML_DIR = BACKEND / 'ml'
DATA_DIR = ML_DIR / 'data'
BASE = DATA_DIR / 'oxford-iiit-pet'
ANNS_CANDIDATES = (
    DATA_DIR / 'annotations' / 'trainval.txt',
    BASE / 'annotations' / 'trainval.txt',
)
LABELS_PATH = ML_DIR / 'breed_labels.json'
WEIGHTS_PATH = ML_DIR / 'breed_classifier.pt'
ANNOTATIONS_URL = 'https://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz'


def _display_name(raw_cls: str) -> str:
    return ' '.join(part.title() for part in raw_cls.split('_'))


def _classes_from_split(split_file: Path) -> list[str]:
    image_ids: list[str] = []
    label_ids: list[int] = []
    with open(split_file, encoding='utf-8') as fh:
        for line in fh:
            image_id, label, _bin_label, _ = line.strip().split()
            image_ids.append(image_id)
            label_ids.append(int(label) - 1)
    pairs = {(image_id.rsplit('_', 1)[0], label) for image_id, label in zip(image_ids, label_ids)}
    return [_display_name(raw) for raw, _ in sorted(pairs, key=lambda item: item[1])]


def ensure_annotations() -> Path:
    for split_file in ANNS_CANDIDATES:
        if split_file.is_file():
            return split_file
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    archive = DATA_DIR / 'annotations.tar.gz'
    if not archive.is_file():
        print(f'Downloading {ANNOTATIONS_URL} ...')
        urllib.request.urlretrieve(ANNOTATIONS_URL, archive)
    print('Extracting annotations...')
    with tarfile.open(archive, 'r:gz') as tar:
        tar.extractall(path=DATA_DIR, filter='data')
    for split_file in ANNS_CANDIDATES:
        if split_file.is_file():
            return split_file
    raise RuntimeError('trainval.txt not found after annotations extraction')


def bootstrap() -> None:
    split_file = ensure_annotations()
    class_names = _classes_from_split(split_file)
    print('Class order:', class_names)
    labels = build_labels(class_names)
    ML_DIR.mkdir(parents=True, exist_ok=True)
    with open(LABELS_PATH, 'w', encoding='utf-8') as fh:
        json.dump(labels, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    print(f'Wrote {len(labels)} labels to {LABELS_PATH}')

    num_classes = len(class_names)
    model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
    model.classifier[3] = nn.Linear(model.classifier[3].in_features, num_classes)
    torch.save(model.state_dict(), WEIGHTS_PATH)
    print(f'Saved bootstrap weights ({num_classes} classes) to {WEIGHTS_PATH}')
    print('For better accuracy run: backend\\venv\\Scripts\\python.exe scripts\\train_breed_model.py')


if __name__ == '__main__':
    bootstrap()
