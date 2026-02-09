# Project Structure

```
etf-tracker/
│
├── .github/
│   └── workflows/
│       └── etf_tracker.yml          # GitHub Actions workflow
│
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
│
├── etf_tracker.py                   # Main tracking script
├── config.py                        # Configuration file
├── requirements.txt                 # Python dependencies
│
├── test_local.py                    # Local testing script
├── setup.sh                         # Quick setup script
├── generate_cronjob_config.py       # Cron-job.org config generator
│
├── README.md                        # Main documentation
├── CONTRIBUTING.md                  # Contribution guidelines
├── CHANGELOG.md                     # Version history
└── PROJECT_STRUCTURE.md            # This file
```

## File Descriptions

### Core Files

**etf_tracker.py**
- Main Python script that fetches data and sends Telegram updates
- Handles NSE data, MCX prices, forex rates, and iNAV calculations
- Class-based design for easy extension

**config.py**
- Configuration settings for ETFs, market hours, APIs
- Easy customization without touching main code
- Alert configuration for future enhancements

**requirements.txt**
- Python package dependencies
- Keep it minimal for faster GitHub Actions runs

### GitHub Actions

**.github/workflows/etf_tracker.yml**
- Automated workflow configuration
- Supports: schedule, manual trigger, webhook
- Runs on Ubuntu with Python 3.11

### Setup & Testing

**setup.sh**
- Quick setup script for local development
- Creates virtual environment
- Installs dependencies
- Sets up .env file

**test_local.py**
- Comprehensive testing before deployment
- Checks environment variables
- Tests API connectivity
- Validates Telegram connection
- Runs actual tracker

**generate_cronjob_config.py**
- Generates cron-job.org configuration
- Creates curl test commands
- Saves config to JSON file

### Documentation

**README.md**
- Complete setup guide
- Feature list
- Troubleshooting
- Usage examples

**CONTRIBUTING.md**
- How to contribute
- Code style guidelines
- Feature ideas
- Pull request process

**CHANGELOG.md**
- Version history
- Release notes
- Planned features

### Configuration

**.env.example**
- Template for environment variables
- Copy to .env for local use
- Add to GitHub Secrets for Actions

**.gitignore**
- Protects sensitive data (.env)
- Ignores Python artifacts
- Excludes generated configs

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions / Cron Job                │
│                   (Triggers every 30 minutes)               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     etf_tracker.py                          │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   NSE Data   │  │  MCX/Intl    │  │  Forex Rate  │    │
│  │  (TATAGOLD,  │  │  Prices      │  │  (USD/INR)   │    │
│  │   TATSILV)   │  │ (Gold/Silver)│  │              │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            ▼                                │
│                   ┌────────────────┐                        │
│                   │ iNAV Calculate │                        │
│                   └────────┬───────┘                        │
│                            │                                │
│                            ▼                                │
│                   ┌────────────────┐                        │
│                   │ Format Message │                        │
│                   └────────┬───────┘                        │
└────────────────────────────┼────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     Telegram Bot API                        │
│                  (Send formatted update)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Your Telegram Chat                        │
│                  (Receive ETF update)                       │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Flow

```
1. Local Development
   ├── Edit code
   ├── Test with: python test_local.py
   └── Verify locally

2. GitHub Setup
   ├── Create repository
   ├── Add secrets (Settings > Secrets)
   ├── Push code
   └── Enable Actions

3. Automation Setup
   ├── GitHub Actions (built-in schedule)
   │   └── Runs automatically every 30 min
   │
   └── Cron-job.org (recommended for reliability)
       ├── Generate config with: python generate_cronjob_config.py
       ├── Create account at cron-job.org
       └── Set up webhook to GitHub

4. Monitoring
   ├── Check Telegram for updates
   ├── View GitHub Actions logs
   └── Monitor cron-job.org dashboard
```

## Customization Points

1. **Add More ETFs**: Edit `config.py` ETFS dictionary
2. **Change Update Frequency**: Modify cron schedule in workflow file
3. **Customize Messages**: Edit `format_telegram_message()` function
4. **Add Alerts**: Implement using ALERT_CONFIG in config.py
5. **Different Data Sources**: Modify API_CONFIG and getter methods

## Security Notes

- Never commit .env file
- Keep GitHub PAT secure
- Rotate tokens periodically
- Use GitHub Secrets for Actions
- Don't expose API keys in logs
