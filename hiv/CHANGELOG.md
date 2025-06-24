# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

> ⚠️ This software is for **Research Use Only (RUO)**. Not for diagnostic or clinical decision-making.

---
## [1.0.0] – 2025-06-23
### Added
- First stable release of ReFocus Assistant for Aldatu's HIV drug resistance product line.
- Reorganized code and packaging to support modular configuration via editable TOML files.
- External configuration files (`config.toml`) can be modified post-installation for assay-specific parameters without requiring rebuild.
- Onedir-based executable structure preserves performance and allows advanced users to inspect or modify internal assets as needed.

### Improved
- Updated `.spec` and build pipeline to support runtime-accessible data (TOML, EULA, README).
- Replaced all relative imports with absolute imports to ensure compatibility with PyInstaller builds.
- Dynamic loading of GUI assets and support files using `sys._MEIPASS` where applicable.
- GUI window icon now loads correctly in both development and executable contexts.
- Application startup errors are now surfaced when run from command-line to support debugging.
- Windows installer built using Inno Setup for clean deployment: user-friendly, self-contained, and runtime-ready.
- Installer re-uploaded on June 24, 2025 to fix a folder conflict issue when installing both PANDAA tools on the same machine. Core executable unchanged.

### Removed
- Removed unnecessary bundling of static configuration files (e.g., TOML) in compiled binary, allowing user-level overrides and editability.

### Build Environment
- Windows: 10.0.19043-SP0
- Python: 3.9.5
- PyInstaller: 6.11.0
- Inno Setup: 6.4.1
- OS tested: Windows 10
- Installer: `ReFocusAssistant_Installer_v1.0.0.exe`
- Certificate: self-signed for internal use (SmartScreen warning expected)

### Dependencies
- pandas 2.2.3
- numpy 1.24.1
- pillow 11.0.0
- reportlab 4.2.5 _(local wheel)_
- pyinstaller-hooks-contrib 2024.9
- pywin32 308
- python-dateutil 2.9.0.post0

### SHA256 Checksums
- Application: `ReFocusAssistant_v1.0.0.exe`  
  `ADB4309F7A7D65F6F15CF8C8570623AD05069970EEE65ADA326F3C7DB6619E3B`

- Installer: `ReFocusAssistant_Installer_v1.0.0.exe`  
  `68E95CAE5CF068917A25BA35002E518F5640E06DCFD1F3BD1EA41A1611E553F8`

### Validation
- Installer tested on clean Windows 10 machine (non-dev environment).
- Double-click-to-launch functionality confirmed.
- TOML editing validated with new assay parameters.
- GUI asset loading, splash screen, result processing all function as expected.
- Help menu, About dialog, and embedded documentation tested and verified.

### Notes
- This release is **Research Use Only (RUO)**. Not for clinical decision-making.
- Application is unsigned and self-signed only for internal testing. Certificate trust warnings are expected unless signed by a recognized Certificate Authority.
- Installer can be redistributed via Aldatu’s website or internal support tools.


## [0.1.1] – 2025-06-11
### Added
- Minor bug fix: corrected build spec file to accomodate TOML files


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
