# Changelog

## [1.0.0] - 2025-02-11

### Fixed
- Corrected base image references to use hassio-addons base images
- Fixed image version to use stable 16.3.2 release
- Updated pip install to use --break-system-packages flag for Alpine compatibility

### Added
- Initial release
- SIP registration support
- Auto-answer incoming calls
- Outgoing call support via API
- RESTful API for call control
- Health check endpoint
- Status monitoring
- Configurable logging levels
- Support for aarch64, amd64, and armv7 architectures

### Features
- Flask-based API server
- PJSUA CLI integration for SIP/VoIP
- Environment-based configuration
- Graceful shutdown handling
