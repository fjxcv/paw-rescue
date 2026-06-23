#!/usr/bin/env python
"""
Fine-tune MobileNetV3-Small on Oxford-IIIT Pet (37 breeds, public dataset).
Run from paw-rescue:
  backend\\venv\\Scripts\\python.exe scripts\\train_breed_model.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'
BACKEND = ROOT / 'backend'
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(SCRIPTS))

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, models, transforms

ML_DIR = BACKEND / 'ml'
LABELS_PATH = ML_DIR / 'breed_labels.json'
WEIGHTS_PATH = ML_DIR / 'breed_classifier.pt'
def train(epochs: int = 2, batch_size: int = 16, max_samples: int = 1500):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    print('Downloading Oxford-IIIT Pet dataset (first run may take a while)...')
    dataset = datasets.OxfordIIITPet(
        root=str(ML_DIR / 'data'),
        download=True,
        transform=transform,
        target_types='category',
    )

    num_classes = len(dataset.classes)
    with open(LABELS_PATH, encoding='utf-8') as f:
        labels = json.load(f)
    if len(labels) != num_classes or any(labels[i]['en'] != dataset.classes[i] for i in range(num_classes)):
        print('Syncing breed_labels.json to dataset class order...')
        from sync_breed_labels import build_labels
        labels = build_labels(list(dataset.classes))
        with open(LABELS_PATH, 'w', encoding='utf-8') as f:
            json.dump(labels, f, ensure_ascii=False, indent=2)
            f.write('\n')

    indices = list(range(min(len(dataset), max_samples)))
    print(f'Training samples: {len(indices)}')

    loader = DataLoader(
        Subset(dataset, indices),
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,
    )

    model = models.mobilenet_v3_small(weights=models.MobileNet_V3_Small_Weights.DEFAULT)
    model.classifier[3] = nn.Linear(model.classifier[3].in_features, num_classes)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    model.train()
    for epoch in range(epochs):
        total_loss = 0.0
        count = 0
        for images, targets in loader:
            images = images.to(device)
            targets = targets.to(device).long()
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            count += 1
        print(f'Epoch {epoch + 1}/{epochs} loss={total_loss / max(count, 1):.4f}')

    ML_DIR.mkdir(parents=True, exist_ok=True)
    torch.save(model.cpu().state_dict(), WEIGHTS_PATH)
    print(f'Saved weights to {WEIGHTS_PATH}')


if __name__ == '__main__':
    train()
