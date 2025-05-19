# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

> ⚠️ This software is for **Research Use Only (RUO)**. Not for diagnostic or clinical decision-making.

---

## [0.1.0] – 2025-05-19
### Added
- Initial public release of ReFocus Assistant. Note that this is a beta version (still in development).
- Companion tool for Aldatu's HIV drug-resistant mutation (DRM) products.
- Windows installer with embedded EULA and ReadMe.
- Automated result analysis from exported files.
- RUO designation included in UI and documentation.

### Build Environment
- Windows: 10.0.19043-SP0
- Python: 3.9.5
- PyInstaller: 6.11.0
- Inno Setup: 6.4.1
- OS tested: Windows 10
- Signed installer: `ReFocusAssistant_Setup_v0.1.0.exe`

### Dependencies
- pandas 2.2.3
- numpy 1.24.1
- pillow 11.0.0
- reportlab 4.2.5  _(local wheel)_
- pyinstaller-hooks-contrib 2024.9
- pywin32 308
- python-dateutil 2.9.0.post0

### SHA256 Checksums
- Application: `ReFocusAssistant_v0.1.0.exe
  `DC85CD01965CB479B4DEF3655C631089BBFDFA07E3F5EC7C088992B5DA174526`

- Installer: `ReFocusAssistant_Installer_v0.1.0.exe`  
  `09996E25875B8817BBAC11BD9DA60D888C52F9A9FFD264AAD38E7404D098D552`

### Validation
- Installation and execution validated on Windows 10.
- Splash screen, file loading, and report generation tested with example dataset.
- Outputs matched expected values for example dataset.

### Certificate Files Notice

During early development of ReFocus Assistant, self-signed digital certificates (`.pfx` and `.cer` files) were created and committed for the purpose of testing code signing procedures using Microsoft's `signtool` utility. These certificates were:

- Not issued by a trusted Certificate Authority (CA)
- Not used to sign any distributed binaries or official releases
- Created exclusively for local experimentation with signing workflows

As of release version v0.1.0, all such test artifacts have been removed from the active repository and `.gitignore`d to prevent inclusion in future commits. No production or company-trusted certificate keys were stored, shared, or published at any point. 

These test files remain accessible in early commit history for reference but pose no security or regulatory risk to product releases. This has been reviewed and deemed acceptable under ISO 13485 software lifecycle documentation and does not affect validated outputs.
