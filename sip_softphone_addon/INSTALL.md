# Installation Instructions

## Method 1: Local Add-on Installation

1. **Copy the addon to your Home Assistant**
   
   Copy the entire `sip_softphone_addon` folder to your Home Assistant's addons directory:
   
   ```
   /addons/sip_softphone/
   ```
   
   Your directory structure should look like:
   ```
   /addons/
     └── sip_softphone/
         ├── config.json
         ├── Dockerfile (or Dockerfile.simple)
         ├── run.sh
         ├── app_simple.py (or app.py + pjsua_wrapper.py)
         ├── build.yaml
         └── README.md
   ```

2. **Choose your Dockerfile**
   
   Two versions are provided:
   
   - **Simple version (recommended)**: Uses PJSUA CLI
     - Rename `Dockerfile.simple` to `Dockerfile`
     - Uses `app_simple.py` (already configured in run.sh)
   
   - **Advanced version**: Uses PJSUA2 Python library
     - Use existing `Dockerfile`
     - Requires compilation, may have build issues

3. **Install via Home Assistant UI**
   
   - Go to **Settings** → **Add-ons**
   - Click **Add-on Store** (bottom right)
   - Click the three dots (top right) → **Check for updates**
   - You should see "SIP Softphone" in the Local Add-ons section
   - Click it and press **Install**

4. **Configure the addon**
   
   Go to the **Configuration** tab and enter:
   
   ```yaml
   sip_server: "sip.yourprovider.com"
   extension: "1000"
   password: "your-sip-password"
   port: 5060
   log_level: "info"
   ```

5. **Start the addon**
   
   - Go to the **Info** tab
   - Toggle **"Start on boot"** if desired
   - Click **Start**
   - Check the **Log** tab to verify it's working

## Method 2: Manual Docker Build (Testing)

If you want to test before installing:

```bash
cd sip_softphone_addon

# Rename the simple Dockerfile
mv Dockerfile.simple Dockerfile

# Build the image
docker build -t sip-softphone:test .

# Run it
docker run -it --rm \
  --network host \
  -e SIP_SERVER="sip.yourprovider.com" \
  -e EXTENSION="1000" \
  -e PASSWORD="your-password" \
  -e PORT=5060 \
  -e LOG_LEVEL="info" \
  sip-softphone:test
```

## Troubleshooting

### Build fails with PJSUA2
- Use the simple version (`Dockerfile.simple`) instead
- The simple version is more reliable and easier to build

### Port 5060 already in use
- Another SIP client might be running
- Change the port in configuration

### Registration fails
- Verify your SIP credentials
- Check if your SIP server is reachable
- Look at the logs for detailed error messages

### No audio on calls
- Ensure `host_network: true` is in config.json
- Check ALSA audio devices are available

## Testing the API

Once running, test the API:

```bash
# Health check
curl http://localhost:8099/health

# Get status
curl http://localhost:8099/status

# Make a call
curl -X POST http://localhost:8099/call \
  -H "Content-Type: application/json" \
  -d '{"destination": "1001"}'

# Send DTMF tones
curl -X POST http://localhost:8099/dtmf \
  -H "Content-Type: application/json" \
  -d '{"digits": "1234"}'

# Hang up
curl -X POST http://localhost:8099/hangup
```

## Next Steps

After installation:
1. Test making a call via the API
2. Set up Home Assistant automations (see README.md)
3. Configure rest_command services
4. Integrate with companion app notifications
