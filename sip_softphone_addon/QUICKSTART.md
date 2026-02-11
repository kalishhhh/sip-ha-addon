# Quick Start Guide - SIP Softphone Add-on

## What You Have

A complete Home Assistant add-on that turns your HA instance into a SIP softphone.

## Files Overview

### Core Files (Required)
- `config.json` - Add-on configuration and metadata
- `Dockerfile.simple` - Docker build instructions (RENAME to `Dockerfile`)
- `run.sh` - Startup script
- `app_simple.py` - Main application (referenced as app.py by run.sh)
- `build.yaml` - Multi-architecture build config

### Documentation
- `README.md` - User documentation
- `INSTALL.md` - Installation instructions
- `CHANGELOG.md` - Version history

### Optional
- `app.py` + `pjsua_wrapper.py` - Advanced version (harder to build)
- `Dockerfile` - Advanced version dockerfile

## Installation (Simple 3 Steps)

### 1. Prepare the Files
```bash
# Rename the simple Dockerfile
mv Dockerfile.simple Dockerfile

# The addon will use app_simple.py automatically via run.sh
```

### 2. Copy to Home Assistant
Copy the entire folder to:
```
/addons/sip_softphone/
```

### 3. Install via UI
- Settings → Add-ons → Add-on Store
- Refresh (three dots menu → Check for updates)
- Find "SIP Softphone" under Local Add-ons
- Click Install

## Configuration

```yaml
sip_server: "sip.yourprovider.com"  # Your SIP server
extension: "1000"                    # Your extension number
password: "secret"                   # Your SIP password
port: 5060                          # SIP port
log_level: "info"                   # Logging: debug/info/warning/error
```

## Usage

### Make a Call from Home Assistant

1. Add to `configuration.yaml`:
```yaml
rest_command:
  sip_call:
    url: "http://localhost:8099/call"
    method: POST
    content_type: "application/json"
    payload: '{"destination": "{{ destination }}"}'
```

2. Create automation:
```yaml
automation:
  - alias: "Call my phone when doorbell rings"
    trigger:
      platform: state
      entity_id: binary_sensor.doorbell
      to: "on"
    action:
      service: rest_command.sip_call
      data:
        destination: "1001"
```

### API Endpoints

All available at `http://localhost:8099/`:

- `GET /health` - Check if running
- `GET /status` - Get registration status
- `POST /call` - Make a call: `{"destination": "1001"}`
- `POST /hangup` - End all calls
- `POST /dtmf` - Send tones: `{"digits": "1234"}`

## Troubleshooting

**Build fails?**
- Make sure you renamed `Dockerfile.simple` to `Dockerfile`

**Can't register?**
- Check SIP credentials in configuration
- Verify SIP server address is correct
- Check logs: Add-ons → SIP Softphone → Log

**No audio?**
- host_network must be enabled (it is by default)

**Port conflict?**
- Change port in configuration if 5060 is used

## Support

Check logs first:
```
Settings → Add-ons → SIP Softphone → Log tab
```

Enable debug logging:
```yaml
log_level: "debug"
```

## What This Does

1. ✅ Registers with your SIP server
2. ✅ Auto-answers incoming calls
3. ✅ Makes outgoing calls via API
4. ✅ Sends DTMF tones
5. ✅ Provides status monitoring
6. ✅ Works with HA automations

Perfect for:
- Doorbell intercom systems
- Emergency call notifications
- Two-way communication
- Home automation voice alerts
