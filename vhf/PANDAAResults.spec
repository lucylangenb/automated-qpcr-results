# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['PANDAAResults.py'],
    pathex=[],
    binaries=[],
    datas=[('*.gif', '.'),
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

splash = Splash('aldatulogo_opaque.png',
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
    name='ReFocusAssistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version.txt',
    icon=['aldatulogo_icon.ico'],
)
