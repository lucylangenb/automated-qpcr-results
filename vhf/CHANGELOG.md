# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

> ⚠️ This software is for **Research Use Only (RUO)**. Not for diagnostic or clinical decision-making.

---

## [1.0.0] – 2025-04-01
### Added
- Initial public release of ReFocus Assistant.
- Companion tool for Aldatu's viral hemorrhagic fever diagnostic products.
- Windows installer with embedded EULA and ReadMe.
- Automated result analysis from exported files.
- RUO designation included in UI and documentation.

### Build Environment
- Windows: 10.0.19043-SP0
- Python: 3.9.5
- PyInstaller: 6.11.0
- Inno Setup: 6.4.1
- OS tested: Windows 10
- Signed installer: `ReFocusAssistant_Setup_v1.0.0.exe`

### Dependencies
- pandas 2.2.3
- numpy 1.24.1
- pillow 11.0.0
- reportlab 4.2.5  _(local wheel)_
- pyinstaller-hooks-contrib 2024.9
- pywin32 308
- python-dateutil 2.9.0.post0

### SHA256 Checksums
- Application: `ReFocusAssistant_v1.0.0.exe`  
  `BAFCD6742C932E875724C709FFA5EE9FD182B26DDC73A0A72C4AAB3BEB12149A`
- Installer: `ReFocusAssistant_v1.0.0_Installer.exe`  
  `FA929312079A7AD28E7CE6EB47ED777C9876B9B484C4402646B1B90C264358BE`

### Validation
- Installation and execution validated on Windows 10.
- Splash screen, file loading, and report generation tested with example dataset.
- Outputs matched expected values for example dataset.

### Certificate Files Notice

During early development of ReFocus Assistant, self-signed digital certificates (`.pfx` and `.cer` files) were created and committed for the purpose of testing code signing procedures using Microsoft's `signtool` utility. These certificates were:

- Not issued by a trusted Certificate Authority (CA)
- Not used to sign any distributed binaries or official releases
- Created exclusively for local experimentation with signing workflows

As of release version v1.0.0, all such test artifacts have been removed from the active repository and `.gitignore`d to prevent inclusion in future commits. No production or company-trusted certificate keys were stored, shared, or published at any point.

These test files remain accessible in early commit history for reference but pose no security or regulatory risk to product releases. This has been reviewed and deemed acceptable under ISO 13485 software lifecycle documentation and does not affect validated outputs.
