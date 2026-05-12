# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

block_cipher = None

SPEC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SPEC_DIR.parent
SCRIPT_PATH = PROJECT_ROOT / "src" / "ppt_renderer" / "cli.py"
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
    [],
    exclude_binaries=True,
    name='ppt-renderer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ppt-renderer',
)
