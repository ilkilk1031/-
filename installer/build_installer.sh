#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python -m pip install -U pip
python -m pip install -e .[dev] pyinstaller build

python -m build
python -m PyInstaller installer/ppt_renderer.spec --noconfirm

mkdir -p dist/install
cp dist/*.whl dist/install/ || true
cp -r dist/ppt-renderer dist/install/ || true
cp README.md dist/install/

echo "Installer artifacts are available under dist/install"
