# Installer Build Guide

## Goal
Generate distributable installation artifacts for the PPT automation program.

## Build outputs
After running the build script, artifacts are created in `dist/install/`:
- Python wheel (`*.whl`) for pip installation
- Standalone executable bundle (`dist/ppt-renderer/`) from PyInstaller
- Project `README.md`

## Build command
```bash
bash installer/build_installer.sh
```

## Install options
### 1) Python package install
```bash
pip install dist/install/ppt_renderer-0.1.0-py3-none-any.whl
ppt-renderer --input examples/sample_input.json --output output/sample_deck.pptx
```

### 2) Standalone executable
```bash
./dist/install/ppt-renderer/ppt-renderer --input examples/sample_input.json --output output/sample_deck.pptx
```

## Notes
- Build is OS-specific for standalone binaries. Build on each target OS.
- If you deploy as API server, use Docker image flow from root `README.md`.
