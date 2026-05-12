# Installer Build Guide

## Goal
Generate distributable installation artifacts for the PPT automation program.

## Build outputs
After running the build script, artifacts are created in `dist/install/`:
- Python wheel (`*.whl`) for pip installation
- Standalone executable bundles (`dist/ppt-renderer/`, `dist/ppt-renderer-ui/`) from PyInstaller
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
python examples/create_sample_asset.py
ppt-renderer --input examples/sample_input.json --output output/sample_deck.pptx
# Fallback when PATH is not configured
python -m ppt_renderer.cli --input examples/sample_input.json --output output/sample_deck.pptx
```

### 2) Standalone executable
```bash
./dist/install/ppt-renderer/ppt-renderer --input examples/sample_input.json --output output/sample_deck.pptx
```

## Notes
- Build is OS-specific for standalone binaries. Build on each target OS.
- If you deploy as API server, use Docker image flow from root `README.md`.

## Windows PATH issue (`ppt-renderer: command not found`)
If pip prints a warning that `ppt-renderer.exe` is installed in a Scripts directory not on PATH, either:
- run with `python -m ppt_renderer.cli ...`, or
- add your Scripts path to PATH and reopen terminal.

Typical path:
`C:\\Users\\<YOUR_USER>\\AppData\\Roaming\\Python\\Python3XX\\Scripts`


## Windows note (Git Bash)
If `pyinstaller: command not found` appears, run module form:
```bash
python -m PyInstaller installer/ppt_renderer.spec --noconfirm
```

The build script already uses module form so PATH setup for Scripts is not required.

## Error: `installer/src/ppt_renderer/cli.py not found`
This happens when PyInstaller resolves relative paths from the wrong working directory.

The spec now uses absolute paths based on its own file location, so rerun:
```bash
bash installer/build_installer.sh
```


## Error: `NameError: __file__ is not defined` in spec
Some PyInstaller runs do not inject `__file__` into the spec namespace.
The spec now falls back to `SPEC` and a default path, then resolves from that location.


### 3) Desktop UI executable
```bash
./dist/install/ppt-renderer-ui/ppt-renderer-ui
```
This launches the desktop UI app directly (no CLI args required).

## Windows PATH issue (`ppt-renderer-ui: command not found`)
If `ppt-renderer-ui` is not found after install, run module form:
```bash
python -m ppt_renderer.gui
```
Or add your Scripts directory to PATH and reopen terminal.
