# SIP Softphone Add-on for Home Assistant

This add-on provides a SIP softphone that can handle voice calls in Home Assistant.

## Features

- ✅ Auto-answer incoming calls
- ✅ Make outgoing calls via API
- ✅ SIP registration with your VoIP provider
- ✅ RESTful API for call control
- ✅ Integration with Home Assistant automations

## Installation

1. Copy this folder to your Home Assistant `addons` directory
2. Reload the Add-on store in Home Assistant
3. Install the "SIP Softphone" add-on
4. Configure your SIP credentials
5. Start the add-on

## Configuration

```yaml
sip_server: "your-sip-server.com"
extension: "1000"
password: "your-password"
port: 5060
log_level: "info"
```

### Options

- `sip_server` (required): Your SIP server address
- `extension` (required): Your SIP extension/username
- `password` (required): Your SIP password
- `port` (optional): SIP port (default: 5060)
- `log_level` (optional): Logging level - debug, info, warning, error (default: info)

## API Endpoints

The add-on exposes a RESTful API on port 8099:

### Make a Call
```bash
POST http://homeassistant.local:8099/call
Content-Type: application/json

{
  "destination": "1001"
}
```

### Hang Up
```bash
POST http://homeassistant.local:8099/hangup
```

### Status
```bash
GET http://homeassistant.local:8099/status
```

### Health Check
```bash
GET http://homeassistant.local:8099/health
```

## Home Assistant Integration

### Make a call from automation:

```yaml
automation:
  - alias: "Call when doorbell pressed"
    trigger:
      - platform: state
        entity_id: binary_sensor.doorbell
        to: "on"
    action:
      - service: rest_command.make_sip_call
        data:
          destination: "1001"
```

Add this to your `configuration.yaml`:

```yaml
rest_command:
  make_sip_call:
    url: "http://localhost:8099/call"
    method: POST
    content_type: "application/json"
    payload: '{"destination": "{{ destination }}"}'
  
  hangup_sip_call:
    url: "http://localhost:8099/hangup"
    method: POST
```

## Troubleshooting

### Check logs
View the add-on logs in the Home Assistant UI or use:
```bash
docker logs addon_sip_softphone
```

### Common issues

1. **Registration failed**: Check your SIP credentials and server address
2. **No audio**: Ensure `host_network: true` is enabled
3. **Port conflicts**: Make sure port 5060 is not used by another service

## Support

For issues and feature requests, please check the GitHub repository.

## License

MIT License
