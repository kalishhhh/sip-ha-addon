# SIP Softphone Setup Checklist

## ✅ Pre-Installation

- [ ] Have SIP server address (e.g., sip.yourprovider.com)
- [ ] Have SIP extension/username (e.g., 1000)
- [ ] Have SIP password
- [ ] Home Assistant is running
- [ ] Can access Home Assistant file system

## ✅ File Preparation

- [ ] Download/extract the `sip_softphone_addon` folder
- [ ] Navigate into the folder
- [ ] Run: `mv Dockerfile.simple Dockerfile`
- [ ] Verify files exist:
  - [ ] config.json
  - [ ] Dockerfile (renamed from Dockerfile.simple)
  - [ ] run.sh
  - [ ] app_simple.py
  - [ ] build.yaml

## ✅ Installation

- [ ] Copy entire folder to `/addons/sip_softphone/` on Home Assistant
- [ ] Go to Settings → Add-ons in Home Assistant UI
- [ ] Click Add-on Store (bottom right)
- [ ] Click ⋮ (three dots) → Check for updates
- [ ] Find "SIP Softphone" under Local Add-ons
- [ ] Click on it
- [ ] Click INSTALL button
- [ ] Wait for installation to complete

## ✅ Configuration

- [ ] Click on Configuration tab
- [ ] Enter your SIP details:
  ```yaml
  sip_server: "sip.yourprovider.com"
  extension: "1000"
  password: "your-password"
  port: 5060
  log_level: "info"
  ```
- [ ] Click SAVE

## ✅ Starting

- [ ] Go to Info tab
- [ ] Enable "Start on boot" (optional)
- [ ] Click START
- [ ] Wait a few seconds
- [ ] Click Log tab
- [ ] Verify you see "SIP Softphone started successfully"
- [ ] Look for "Registration status: OK" or similar

## ✅ Testing

### Test 1: Health Check
```bash
curl http://homeassistant.local:8099/health
```
Expected: `{"status": "healthy", "sip_registered": true}`

### Test 2: Status
```bash
curl http://homeassistant.local:8099/status
```
Expected: `{"registered": true, "server": "...", "extension": "..."}`

### Test 3: Make a Test Call
```bash
curl -X POST http://homeassistant.local:8099/call \
  -H "Content-Type: application/json" \
  -d '{"destination": "1001"}'
```
Expected: `{"status": "success", "message": "Call initiated to 1001"}`

### Test 4: Hang Up
```bash
curl -X POST http://homeassistant.local:8099/hangup
```
Expected: `{"status": "success", "message": "Call hung up"}`

## ✅ Home Assistant Integration

- [ ] Add to `configuration.yaml`:
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
  ```
- [ ] Restart Home Assistant
- [ ] Test service in Developer Tools → Services:
  - Service: `rest_command.sip_call`
  - Service Data: `{"destination": "1001"}`

## ✅ Create Automation (Example)

```yaml
automation:
  - alias: "Call when doorbell pressed"
    trigger:
      - platform: state
        entity_id: binary_sensor.doorbell
        to: "on"
    action:
      - service: rest_command.sip_call
        data:
          destination: "1001"
```

## 🔧 Troubleshooting

If something doesn't work:

1. **Check Logs**
   - Go to Add-ons → SIP Softphone → Log
   - Look for error messages

2. **Common Issues**
   - Registration failed → Check SIP credentials
   - Port in use → Change port in config
   - Build failed → Make sure you renamed Dockerfile.simple to Dockerfile
   - Can't access API → Check if addon is running

3. **Enable Debug Logging**
   - Configuration → `log_level: "debug"`
   - Save and Restart

4. **Test SIP Server Connectivity**
   ```bash
   ping sip.yourprovider.com
   ```

## 📝 Notes

- The addon auto-answers incoming calls
- API runs on port 8099
- SIP runs on port 5060 (configurable)
- Use `host_network: true` for best results (default)

## ✅ Success Indicators

You've successfully installed when:
- [ ] Add-on shows as "Started" in Home Assistant
- [ ] Logs show "SIP Softphone started successfully"
- [ ] Logs show registration is successful
- [ ] Health endpoint returns healthy status
- [ ] You can make a test call via API
- [ ] rest_command services work in HA

---

**Need Help?**
- Check QUICKSTART.md for quick reference
- Check README.md for detailed documentation
- Check INSTALL.md for installation details
- Review logs for error messages
