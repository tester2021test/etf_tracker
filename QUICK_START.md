# 🚀 Quick Reference Guide

## One-Time Setup (5 minutes)

### 1. Get Telegram Bot Credentials
```bash
# Talk to @BotFather on Telegram
# Send: /newbot
# Get: BOT_TOKEN

# Get your Chat ID from @userinfobot
# Or visit: https://api.telegram.org/bot<TOKEN>/getUpdates
```

### 2. Local Testing (Optional)
```bash
chmod +x setup.sh
./setup.sh                    # Install dependencies
cp .env.example .env          # Create environment file
nano .env                     # Add your credentials
python test_local.py          # Test everything
```

### 3. GitHub Setup
```bash
# Create new repository on GitHub
git init
git add .
git commit -m "Initial commit: ETF Tracker"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

# Add Secrets in GitHub:
# Settings > Secrets and variables > Actions > New repository secret
# - TELEGRAM_BOT_TOKEN
# - TELEGRAM_CHAT_ID
```

### 4. Cron-Job.org Setup (Recommended)
```bash
# Generate config
python generate_cronjob_config.py

# Sign up at cron-job.org
# Create new cron job with generated config
# Schedule: */30 * * * *
```

## Daily Usage

**No manual work needed!** Updates arrive automatically every 30 minutes.

## Manual Trigger

### Via GitHub UI
1. Go to Actions tab
2. Click "ETF Tracker - Telegram Updates"
3. Click "Run workflow"

### Via cURL
```bash
# Test repository dispatch
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"event_type":"etf-update"}' \
  https://api.github.com/repos/USERNAME/REPO/dispatches
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No messages | Check GitHub Actions logs |
| Wrong data | NSE API might be down, wait and retry |
| Bot not responding | Verify bot token with: `https://api.telegram.org/botTOKEN/getMe` |
| Actions not running | Enable in Settings > Actions > General |

## Key Commands

```bash
# Local testing
python test_local.py

# Run tracker once
python etf_tracker.py

# Generate cron config
python generate_cronjob_config.py

# Check logs
tail -f *.log  # If you add logging
```

## File Locations

| File | Purpose |
|------|---------|
| `etf_tracker.py` | Main script |
| `config.py` | Settings |
| `.env` | Your credentials (local) |
| `.github/workflows/etf_tracker.yml` | GitHub Actions |

## URLs You'll Need

- Telegram BotFather: https://t.me/botfather
- Get Chat ID: https://t.me/userinfobot
- Cron-Job.org: https://cron-job.org
- GitHub Actions: https://github.com/USERNAME/REPO/actions

## Update Frequency Options

Edit `.github/workflows/etf_tracker.yml`:

```yaml
# Every 15 minutes
- cron: '*/15 * * * *'

# Every hour
- cron: '0 * * * *'

# Market hours only (Mon-Fri, 9am-3pm)
- cron: '0 9-15 * * 1-5'

# Every 30 minutes during market hours
- cron: '*/30 9-15 * * 1-5'
```

## Message Format Preview

```
📊 ETF TRACKER UPDATE
⏰ 09-Feb-2026 02:30 PM IST
📈 Market Status: 🟢 OPEN
...
```

## Support

- GitHub Issues: Report bugs
- Discussions: Ask questions
- PR Welcome: Contribute features

## Quick Tips

💡 **Tip 1**: Use cron-job.org for reliability (GitHub Actions may delay)

💡 **Tip 2**: Test locally before deploying to catch errors early

💡 **Tip 3**: Keep your GitHub token secure and rotate regularly

💡 **Tip 4**: Check GitHub Actions usage limits (2000 min/month free)

💡 **Tip 5**: iNAV is indicative - always verify with official NAV

## Next Steps

1. ✅ Get it running
2. ⭐ Star the repo
3. 🔔 Watch for updates
4. 🤝 Contribute improvements
5. 📢 Share with other investors

---

**Need help?** Check README.md for detailed documentation.
