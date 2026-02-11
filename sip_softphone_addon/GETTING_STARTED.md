# Getting Started - SIP Softphone Add-on for Home Assistant

## 🎯 What This Does

This add-on turns your Home Assistant into a SIP softphone that can:
- ✅ Make outgoing calls to any SIP number
- ✅ Receive and auto-answer incoming calls
- ✅ Send DTMF tones during calls
- ✅ Integrate with Home Assistant automations
- ✅ Control calls via REST API

## 🚀 Quick Install (5 Minutes)

### Step 1: Prepare Files (30 seconds)
```bash
cd sip_softphone_addon
mv Dockerfile.simple Dockerfile
```

### Step 2: Copy to Home Assistant (1 minute)
Copy the entire `sip_softphone_addon` folder to your Home Assistant:
```
/addons/sip_softphone/
```

**How to access /addons folder:**
- **Samba Share**: `\\homeassistant.local\addons\`
- **SSH/Terminal**: `/addons/`
- **File Editor add-on**: Use the file browser

### Step 3: Install via UI (2 minutes)
1. Open Home Assistant
2. Go to **Settings** → **Add-ons**
3. Click **Add-on Store** (bottom right)
4. Click **⋮** (top right) → **Check for updates**
5. Scroll to **Local Add-ons** section
6. Click **SIP Softphone**
7. Click **INSTALL**
8. Wait for build to complete

### Step 4: Configure (1 minute)
1. Click **Configuration** tab
2. Enter your settings:
```yaml
sip_server: "sip.yourprovider.com"
extension: "1000"
password: "your-sip-password"
port: 5060
log_level: "info"
```
3. Click **SAVE**

### Step 5: Start (30 seconds)
1. Click **Info** tab
2. Toggle **Start on boot** (optional)
3. Click **START**
4. Click **Log** tab to verify

✅ **You should see**: "SIP Softphone started successfully"

## 📞 Test Your Setup

### Quick Test via Terminal
```bash
# Check if it's running
curl http://homeassistant.local:8099/health

# Make a test call (replace 1001 with a real number)
curl -X POST http://homeassistant.local:8099/call \
  -H "Content-Type: application/json" \
  -d '{"destination": "1001"}'
```

### Test via Home Assistant

1. **Add REST commands** to `configuration.yaml`:
```yaml
rest_command:
  sip_call:
    url: "http://localhost:8099/call"
    method: POST
    content_type: "application/json"
    payload: '{"destination": "{{ destination }}"}'
  
  sip_hangup:
    url: "http://localhost:8099/hangup"
    method: POST
  
  sip_dtmf:
    url: "http://localhost:8099/dtmf"
    method: POST
    content_type: "application/json"
    payload: '{"digits": "{{ digits }}"}'
```

2. **Restart Home Assistant**

3. **Test in Developer Tools**:
   - Go to Developer Tools → Services
   - Select `rest_command.sip_call`
   - Enter: `{"destination": "1001"}`
   - Click **CALL SERVICE**

## 🏠 Use Cases & Examples

### Example 1: Doorbell Notification
Call your phone when someone rings the doorbell:

```yaml
automation:
  - alias: "Call me when doorbell rings"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_doorbell
        to: "on"
    action:
      - service: rest_command.sip_call
        data:
          destination: "{{ states('input_text.my_extension') }}"
```

### Example 2: Emergency Alert
Call multiple numbers in case of emergency:

```yaml
automation:
  - alias: "Emergency - Water Leak Detected"
    trigger:
      - platform: state
        entity_id: binary_sensor.water_leak
        to: "on"
    action:
      - repeat:
          count: 3
          sequence:
            - service: rest_command.sip_call
              data:
                destination: "1001"  # Your phone
            - delay: "00:00:30"
            - service: rest_command.sip_hangup
            - delay: "00:00:10"
```

### Example 3: Intercom System
Create a two-way intercom:

```yaml
script:
  call_front_door_intercom:
    alias: "Call Front Door Intercom"
    sequence:
      - service: rest_command.sip_call
        data:
          destination: "2000"  # Intercom extension
      - service: notify.mobile_app
        data:
          title: "Intercom Active"
          message: "Connected to front door"
```

### Example 4: Voice Unlock with DTMF
Send DTMF code to unlock door:

```yaml
script:
  unlock_door_via_phone:
    alias: "Unlock Door Via Phone"
    sequence:
      - service: rest_command.sip_call
        data:
          destination: "3000"  # Door controller
      - delay: "00:00:02"
      - service: rest_command.sip_dtmf
        data:
          digits: "1234#"  # Your unlock code
      - delay: "00:00:01"
      - service: rest_command.sip_hangup
```

## 🔧 API Reference

All endpoints are available at `http://localhost:8099/`

### GET /health
Check if softphone is running
```bash
curl http://localhost:8099/health
```
Response: `{"status": "healthy", "sip_registered": true}`

### GET /status
Get registration status
```bash
curl http://localhost:8099/status
```
Response: `{"registered": true, "server": "...", "extension": "..."}`

### POST /call
Make an outgoing call
```bash
curl -X POST http://localhost:8099/call \
  -H "Content-Type: application/json" \
  -d '{"destination": "1001"}'
```
Response: `{"status": "success", "message": "Call initiated to 1001"}`

### POST /hangup
Hang up all active calls
```bash
curl -X POST http://localhost:8099/hangup
```
Response: `{"status": "success", "message": "Call hung up"}`

### POST /dtmf
Send DTMF tones
```bash
curl -X POST http://localhost:8099/dtmf \
  -H "Content-Type: application/json" \
  -d '{"digits": "1234"}'
```
Response: `{"status": "success", "message": "DTMF sent: 1234"}`

## 🐛 Troubleshooting

### Add-on won't start
1. Check logs: **Add-ons** → **SIP Softphone** → **Log**
2. Verify configuration is correct
3. Ensure SIP server is reachable

### Registration fails
- ✅ Double-check SIP server address
- ✅ Verify extension and password
- ✅ Check if your provider requires a specific port
- ✅ Enable debug logging: `log_level: "debug"`

### Build fails
- ✅ Make sure you renamed `Dockerfile.simple` to `Dockerfile`
- ✅ Try rebuilding: Uninstall and install again
- ✅ Check Home Assistant logs

### No audio on calls
- ✅ Verify `host_network: true` in config.json (default)
- ✅ Check if ALSA audio is available on your system
- ✅ Review PJSUA logs for audio errors

### API not responding
- ✅ Check if add-on is running
- ✅ Verify port 8099 is not blocked
- ✅ Try accessing from the host: `curl http://localhost:8099/health`

### Port 5060 conflict
- Change port in configuration
- Restart the add-on

## 📚 Additional Resources

- **QUICKSTART.md** - Quick reference guide
- **INSTALL.md** - Detailed installation
- **README.md** - Full documentation
- **SETUP_CHECKLIST.md** - Step-by-step checklist
- **FILE_STRUCTURE.md** - File organization

## 💡 Tips & Best Practices

1. **Start Simple**: Test with a single call before building complex automations
2. **Use Variables**: Store numbers in input_text helpers for easy changes
3. **Add Delays**: Give PJSUA time to establish connections
4. **Monitor Logs**: Keep an eye on logs when testing
5. **Debug Mode**: Enable when troubleshooting: `log_level: "debug"`
6. **Backup Config**: Save your working configuration

## 🔐 Security Notes

- Keep your SIP password secure
- Don't expose port 8099 to the internet without authentication
- Use HTTPS/SSL if exposing externally
- Consider firewall rules for SIP ports

## ⚡ Performance

- Lightweight: ~50MB RAM usage
- Fast startup: <10 seconds
- Auto-reconnect on network issues
- Supports multiple architectures

## 🎉 You're All Set!

Your Home Assistant can now make and receive phone calls!

**Next Steps:**
1. Create your first automation
2. Test incoming call auto-answer
3. Explore DTMF tone sending
4. Build custom scripts

Happy calling! 📞
