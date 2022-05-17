# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['EAM Checklist Clicker.py'],
             pathex=[],
             binaries=[],
             datas=[('./targets/target_amazonrme.png', '.'), ('./targets/target_processing.png', '.'), ('./targets/target_checkbox_checked.png', '.'), ('./targets/target_prompt_icon.png', '.'), ('./targets/target_yes_en.png', '.'), ('./targets/target_yes_pl.png', '.'), ('./targets/target_yes_de.png', '.'), ('./targets/target_completed_pl.png', '.'), ('./targets/target_completed_en.png', '.'), ('./targets/target_completed_de.png', '.'), ('./targets/target_employee_pl.png', '.'), ('./targets/target_employee_en.png', '.'), ('./targets/target_employee_de.png', '.')],
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
          name='EAM Checklist Clicker',
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
          entitlements_file=None , icon='EAM Checklist Clicker.ico')
