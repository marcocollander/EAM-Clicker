# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['targetsEAM Checklist Clicker.py'],
             pathex=[],
             binaries=[],
             datas=[('./targetstarget_amazonrme.png', '.'), ('./targetstarget_processing.png', '.'), ('./targetstarget_checkbox_checked.png', '.'), ('./targetstarget_prompt_icon.png', '.'), ('./targetstarget_yes_en.png', '.'), ('./targetstarget_yes_pl.png', '.'), ('./targetstarget_yes_de.png', '.'), ('./targetstarget_completed_pl.png', '.'), ('./targetstarget_completed_en.png', '.'), ('./targetstarget_completed_de.png', '.'), ('./targetstarget_employee_pl.png', '.'), ('./targetstarget_employee_en.png', '.'), ('./targetstarget_employee_de.png', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='targetsEAM Checklist Clicker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='targetsEAM Checklist Clicker.ico')
