# -*- mode: python -*-

block_cipher = None


a = Analysis(['play_game.py'],
             pathex=['C:\\Users\\hallowf\\Desktop\\Git\\GD_AI\\src', '..\\env\\Lib\\'],
             binaries=[],
             datas=[],
             hiddenimports=['h5py','h5py.defs','h5py.utils','h5py.h5ac','h5py._proxy'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Dino_AI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
