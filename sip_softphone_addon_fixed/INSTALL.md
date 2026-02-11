# Installation Guide - FIXED VERSION

## What Was Fixed

The previous version had these issues:
1. ❌ Wrong base image: `ghcr.io/homeassistant/aarch64-addon-base:1.0.0` (doesn't exist)
2. ❌ Image version `1.0.0` not available

## What's Fixed Now

1. ✅ Using correct base: `ghcr.io/hassio-addons/base/aarch64:16.3.2`
2. ✅ Stable version that exists and works
3. ✅ Added `--break-system-packages` flag for pip (Alpine compatibility)

## Quick Install

### 1. Copy to Home Assistant

Copy this entire folder to:
```
/addons/sip_softphone/
```

**Access methods:**
- **Samba**: `\\homeassistant.local\addons\sip_softphone\`
- **SSH**: `/addons/sip_softphone/`
- **File Editor**: Use the file browser

### 2. Install via UI

1. Open Home Assistant
2. Go to **Settings** → **Add-ons**
3. Click **Add-on Store** (bottom right)
4. Click **⋮** (three dots, top right) → **Reload**
5. Scroll to **Local Add-ons**
6. Click **SIP Softphone**
7. Click **INSTALL**
8. Wait for build (may take 5-10 minutes)

### 3. Configure

Click **Configuration** tab:

```yaml
sip_server: "sip.yourprovider.com"
extension: "1000"
password: "your-password"
port: 5060
log_level: "info"
```

Click **SAVE**

### 4. Start

1. Click **Info** tab
2. Enable **Start on boot** (optional)
3. Click **START**
4. Click **Log** tab to verify

## Verify Installation

Check logs for:
```
✅ "Starting SIP Softphone..."
✅ "PJSUA started successfully"
✅ "Starting API server on port 8099..."
```

## Test API

```bash
# Health check
curl http://homeassistant.local:8099/health

# Should return:
# {"status": "healthy", "sip_registered": true}
```

## Troubleshooting

### If build still fails:

1. **Check your architecture**:
   ```bash
   uname -m
   ```
   - `aarch64` = ARM 64-bit (Raspberry Pi 4, etc.)
   - `x86_64` or `amd64` = Intel/AMD 64-bit
   - `armv7l` = ARM 32-bit (Raspberry Pi 3, etc.)

2. **Check base image availability**:
   The addon will automatically use the correct base image for your architecture.

3. **Enable debug logging**:
   In configuration:
   ```yaml
   log_level: "debug"
   ```

4. **Check Docker/Supervisor status**:
   ```bash
   ha supervisor info
   ```

### Common Issues

**"Failed to get token from ghcr.io"**
- This is usually temporary
- Wait a few minutes and try again
- Check internet connection

**"Can't install base image"**
- Verify Home Assistant can reach ghcr.io
- Try restarting Home Assistant
- Check if there are network/firewall issues

**Build takes too long**
- First build can take 10-15 minutes
- Be patient, especially on slower hardware
- Check logs for progress

## Files in This Package

```
sip_softphone/
├── config.json          ✅ FIXED: Removed wrong image field
├── Dockerfile           ✅ FIXED: Added --break-system-packages
├── build.yaml           ✅ FIXED: Correct base images
├── run.sh               ✅ Working
├── app_simple.py        ✅ Working
├── README.md            ✅ Documentation
└── CHANGELOG.md         ✅ Version history
```

## Next Steps After Installation

1. **Test basic call**:
   ```bash
   curl -X POST http://homeassistant.local:8099/call \
     -H "Content-Type: application/json" \
     -d '{"destination": "1001"}'
   ```

2. **Set up Home Assistant integration**:
   Add to `configuration.yaml`:
   ```yaml
   rest_command:
     sip_call:
       url: "http://localhost:8099/call"
       method: POST
       content_type: "application/json"
       payload: '{"destination": "{{ destination }}"}'
   ```

3. **Create an automation**:
   ```yaml
   automation:
     - alias: "Test SIP Call"
       trigger:
         - platform: state
           entity_id: input_boolean.test_call
           to: "on"
       action:
         - service: rest_command.sip_call
           data:
             destination: "1001"
   ```

## Support

If you still have issues:
1. Check the **Log** tab in the addon
2. Enable debug logging
3. Share logs when asking for help
