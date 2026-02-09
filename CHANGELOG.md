# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-09

### Added
- Initial release of ETF Tracker
- Real-time tracking for TATAGOLD and TATSILV ETFs
- iNAV (Indicative NAV) calculation
- International gold/silver spot price tracking
- USD/INR forex rate monitoring
- Premium/Discount analysis
- Market status detection (Open/Closed)
- Telegram bot integration for updates
- GitHub Actions workflow for automation
- Support for cron-job.org webhook triggers
- Comprehensive documentation (README.md)
- Local testing script (test_local.py)
- Configuration file (config.py)
- Environment variable template (.env.example)
- Quick setup script (setup.sh)
- Cron-job configuration generator
- Contributing guidelines

### Features
- ✅ 30-minute automated updates
- ✅ Volume and value tracking
- ✅ Performance comparison between gold and silver
- ✅ Formatted Telegram messages with emojis
- ✅ Error handling and fallbacks
- ✅ Market hours awareness
- ✅ Multiple data sources (NSE, international markets, forex)

### Technical
- Python 3.11 support
- Minimal dependencies (requests, pytz)
- GitHub Actions workflow
- Repository dispatch webhook support
- Session management for NSE API
- Timezone-aware datetime handling

## [Unreleased]

### Planned Features
- Historical data tracking
- Price alerts
- Additional ETFs support
- Web dashboard
- Database integration
- Portfolio tracking
- Machine learning predictions
- Multi-language support

---

## Release Notes

### Version 1.0.0

This is the first stable release of ETF Tracker. The system is production-ready and includes:

**Core Functionality:**
- Automated tracking of TATA Gold and Silver ETFs
- Real-time NAV and iNAV calculations
- International commodity price monitoring
- Forex rate tracking

**Deployment:**
- GitHub Actions for automation
- cron-job.org webhook support
- Easy setup with templates and scripts

**Documentation:**
- Comprehensive README with setup instructions
- Contributing guidelines
- Environment variable templates
- Testing tools

For detailed setup instructions, see [README.md](README.md)

---

[1.0.0]: https://github.com/yourusername/etf-tracker/releases/tag/v1.0.0
