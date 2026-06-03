#!/usr/bin/env python

"""

Ensure breed_classifier.pt exists; bootstrap locally if missing.

  backend\\venv\\Scripts\\python.exe scripts\\download_breed_model.py



Bootstrap uses Oxford annotations + ImageNet MobileNetV3 head (fast).

Fine-tune on full dataset: scripts\\train_breed_model.py

"""

from __future__ import annotations



import subprocess

import sys

from pathlib import Path



ROOT = Path(__file__).resolve().parent.parent

WEIGHTS = ROOT / 'backend' / 'ml' / 'breed_classifier.pt'

BOOTSTRAP = ROOT / 'scripts' / 'bootstrap_breed_model.py'

TRAIN = ROOT / 'scripts' / 'train_breed_model.py'

PYTHON = ROOT / 'backend' / 'venv' / 'Scripts' / 'python.exe'





def main():

    if WEIGHTS.is_file():

        print(f'Model already exists: {WEIGHTS}')

        return 0



    python = str(PYTHON) if PYTHON.is_file() else sys.executable

    print('Weights not found. Running fast bootstrap (annotations + ImageNet backbone)...')

    subprocess.check_call([python, str(BOOTSTRAP)], cwd=str(ROOT))

    if not WEIGHTS.is_file() and TRAIN.is_file():

        print('Bootstrap failed; trying full Oxford training (slow download)...')

        subprocess.check_call([python, str(TRAIN)], cwd=str(ROOT))

    print('Done.')

    return 0





if __name__ == '__main__':

    raise SystemExit(main())

