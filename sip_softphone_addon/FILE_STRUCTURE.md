# SIP Softphone Add-on - File Structure

```
sip_softphone/
├── config.json              # Add-on configuration (REQUIRED)
├── Dockerfile               # Advanced build (optional)
├── Dockerfile.simple        # Simple build (RENAME to Dockerfile - RECOMMENDED)
├── run.sh                   # Startup script (REQUIRED)
├── build.yaml               # Build configuration (REQUIRED)
│
├── app.py                   # Advanced Python app with PJSUA2
├── pjsua_wrapper.py         # PJSUA2 wrapper library
├── app_simple.py            # Simple Python app with PJSUA CLI (RECOMMENDED)
│
├── README.md                # User documentation
├── QUICKSTART.md            # Quick start guide
├── INSTALL.md               # Installation instructions
├── CHANGELOG.md             # Version history
├── ICON_README.txt          # Icon instructions
└── .gitignore               # Git ignore rules
```

## Recommended Setup (Easiest to Build)

**Use these files:**
1. `config.json` ✓
2. `Dockerfile.simple` → rename to `Dockerfile` ✓
3. `run.sh` ✓
4. `build.yaml` ✓
5. `app_simple.py` (automatically used) ✓

**Skip these files:**
- `app.py` (only if you want advanced PJSUA2)
- `pjsua_wrapper.py` (only if you want advanced PJSUA2)
- Original `Dockerfile` (only if you want advanced PJSUA2)

## File Descriptions

### config.json
Defines the add-on metadata, options, and schema for Home Assistant.

### Dockerfile.simple (RECOMMENDED)
Simpler Docker build using PJSUA CLI instead of PJSUA2 library.
- Easier to compile
- Fewer dependencies
- More reliable builds
- Same functionality

### Dockerfile (ADVANCED)
Complex Docker build using PJSUA2 Python bindings.
- Requires compilation
- More dependencies
- May have build issues on some architectures

### run.sh
Bash script that:
- Reads configuration from Home Assistant
- Validates settings
- Exports environment variables
- Starts the Python application

### app_simple.py (RECOMMENDED)
Python application using PJSUA CLI:
- Controls PJSUA via command-line interface
- Provides REST API on port 8099
- Handles calls, hangup, DTMF, status

### app.py + pjsua_wrapper.py (ADVANCED)
Python application using PJSUA2 library:
- Direct Python bindings to PJSIP
- More control but harder to build
- Use only if you need advanced features

### build.yaml
Specifies base Docker images for different architectures:
- aarch64 (ARM 64-bit, e.g., Raspberry Pi 4)
- amd64 (Intel/AMD 64-bit)
- armv7 (ARM 32-bit, e.g., Raspberry Pi 3)

## Quick Setup Commands

```bash
# 1. Navigate to the addon folder
cd sip_softphone_addon

# 2. Use the simple version (recommended)
mv Dockerfile.simple Dockerfile

# 3. Copy to Home Assistant
# Copy entire folder to: /addons/sip_softphone/
```

Then install via Home Assistant UI.
