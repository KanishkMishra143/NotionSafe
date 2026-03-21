# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# List all data files to include (e.g., icons, logos)
added_files = [
    ('assets/logo.png', 'assets'),
]

# Hidden imports that PyInstaller might miss
hidden_imports = [
    'keyring.backends.Windows',
    'PySide6.QtXml',
    'notion2md.__main__',
    'notion2md.exporter',
]

a = Analysis(
    ['notebackup/__main__.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
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
    name='NotionSafe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Console Subsystem: Necessary for CLI to behave correctly
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/logo.png'],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NotionSafe', # This creates the dist/NotionSafe/ folder
)
