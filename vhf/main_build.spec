# -*- mode: python ; coding: utf-8 -*-

import sys, os

shared_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'shared'))
shared_assets_path = (os.path.join(shared_path, 'assets'))

splash_image_path = (
    os.path.join(sys._MEIPASS, 'aldatulogo_opaque.png')
    if hasattr(sys, '_MEIPASS')
    else os.path.join(shared_assets_path, 'aldatulogo_opaque.png'))
ico_path = (
    os.path.join(sys._MEIPASS, 'aldatulogo_icon.ico')
    if hasattr(sys, '_MEIPASS')
    else os.path.join(shared_assets_path, 'aldatulogo_icon.ico'))

version=open('version_number.txt').read().strip()

a = Analysis(
    ['main.py'],
    pathex=[shared_path],
    binaries=[],
    datas=[(os.path.join(shared_assets_path, 'aldatulogo_icon.gif'), '.'),
           (os.path.join(shared_assets_path, 'aldatulogo.gif'), '.'),
           (os.path.join(shared_assets_path, 'aldatulogo_icon.ico'), '.'),
           ('version_number.txt', '.'),
           ('eula.txt', '.'),
           ('readme.txt', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

splash = Splash(splash_image_path,
                binaries=a.binaries,
                datas=a.datas,
                text_pos=(20,30),
                text_size=9,
                text_color='#204771',
                text_font='Arial')

exe = EXE(
    pyz,
    a.scripts,
    splash,
    splash.binaries,
    a.binaries,
    a.datas,
    [],
    exclude_binaries=True,
    name='EpiFocusAssistant_v'+version,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_v{}.txt'.format(version),
    icon=[ico_path]
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EpiFocusAssistant_v'+version
)
