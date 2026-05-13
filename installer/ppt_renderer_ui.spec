# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

block_cipher = None

_spec_ref = globals().get("__file__") or globals().get("SPEC") or "installer/ppt_renderer_ui.spec"
SPEC_DIR = Path(_spec_ref).resolve().parent
PROJECT_ROOT = SPEC_DIR.parent
SCRIPT_PATH = PROJECT_ROOT / "src" / "ppt_renderer" / "gui.py"
SAMPLE_INPUT_PATH = PROJECT_ROOT / "examples" / "sample_input.json"


a = Analysis(
    [str(SCRIPT_PATH)],
    pathex=[str(PROJECT_ROOT / "src")],
    binaries=[],
    datas=[(str(SAMPLE_INPUT_PATH), "examples")],
    hiddenimports=['ppt_renderer'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ppt-renderer-ui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
