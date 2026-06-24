import json
import time
from io import BytesIO
from pathlib import Path

import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import models, transforms

ML_DIR = Path(__file__).resolve().parent.parent / 'ml'
LABELS_PATH = ML_DIR / 'breed_labels.json'
WEIGHTS_PATH = ML_DIR / 'breed_classifier.pt'

_MODEL = None
_LABELS = None
_TRANSFORM = None
_NUM_CLASSES = 37


class BreedModelNotReadyError(Exception):
    pass


def model_paths():
    return {'labels': str(LABELS_PATH), 'weights': str(WEIGHTS_PATH)}


def is_model_ready() -> bool:
    return WEIGHTS_PATH.is_file() and LABELS_PATH.is_file()


def _load_labels():
    global _LABELS
    if _LABELS is None:
        with open(LABELS_PATH, encoding='utf-8') as f:
            _LABELS = json.load(f)
    return _LABELS


def _build_model(num_classes: int):
    model = models.mobilenet_v3_small(weights=None)
    model.classifier[3] = torch.nn.Linear(model.classifier[3].in_features, num_classes)
    return model


def _load_model():
    global _MODEL, _TRANSFORM
    if not is_model_ready():
        raise BreedModelNotReadyError(
            'Breed model weights not found. Run: backend\\venv\\Scripts\\python.exe scripts\\train_breed_model.py'
        )
    if _MODEL is None:
        labels = _load_labels()
        num_classes = len(labels)
        _MODEL = _build_model(num_classes)
        state = torch.load(WEIGHTS_PATH, map_location='cpu')
        _MODEL.load_state_dict(state)
        _MODEL.eval()
        _TRANSFORM = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])
    return _MODEL, _TRANSFORM


def predict_breeds(image_bytes: bytes, top_k: int = 4) -> list[dict]:
    labels = _load_labels()
    model, transform = _load_model()
    image = Image.open(BytesIO(image_bytes)).convert('RGB')
    tensor = transform(image).unsqueeze(0)
    started = time.perf_counter()
    with torch.no_grad():
        logits = model(tensor)
        probs = F.softmax(logits, dim=1)[0]
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    k = min(top_k, len(labels))
    top_probs, top_idx = probs.topk(k)
    results = []
    for prob, idx in zip(top_probs.tolist(), top_idx.tolist()):
        item = labels[idx]
        results.append({
            'breed': item['zh'],
            'species': item['species'],
            'confidence': round(float(prob), 2),
            'en': item['en'],
        })
    return results, elapsed_ms
