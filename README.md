# 📊 TATSILV & TATAGOLD ETF Tracker

Automated Telegram bot that sends updates every 30 minutes with:
- Real-time NAV tracking for TATA Gold & Silver ETFs
- iNAV (Indicative NAV) calculation
- MCX commodity prices
- USD/INR forex rates
- Premium/Discount analysis
- Performance metrics

## 🚀 Features

- ✅ Real-time NSE data for TATAGOLD and TATSILV
- ✅ International gold/silver spot prices (USD/oz)
- ✅ Automatic iNAV calculation
- ✅ Premium/Discount tracking vs iNAV
- ✅ Market status detection (Open/Closed)
- ✅ Volume and value tracking
- ✅ Forex rate monitoring (USD/INR)
- ✅ Performance comparison
- ✅ Runs every 30 minutes automatically
- ✅ Can be triggered via cron-job.org webhook

## 📋 Prerequisites

1. **Telegram Bot**
   - Create a bot via [@BotFather](https://t.me/botfather)
   - Get your `BOT_TOKEN`
   - Get your `CHAT_ID` (use [@userinfobot](https://t.me/userinfobot))

2. **GitHub Account**
   - Repository to host this code

3. **Optional: Gold API Key**
   - Sign up at [goldapi.io](https://www.goldapi.io/) for better gold price data
   - Free tier available

## 🛠️ Setup Instructions

### Step 1: Create Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow instructions and get your `BOT_TOKEN`
4. Get your `CHAT_ID`:
   - Send a message to [@userinfobot](https://t.me/userinfobot)
   - Or send a message to your bot and visit:
     ```
     https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
     ```

### Step 2: Fork/Clone this Repository

```bash
git clone https://github.com/yourusername/etf-tracker.git
cd etf-tracker
```

### Step 3: Configure GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:

| Secret Name | Description | Required |
|------------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from BotFather | ✅ Yes |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | ✅ Yes |
| `GOLD_API_KEY` | API key from goldapi.io | ⚠️ Optional |

### Step 4: Enable GitHub Actions

1. Go to your repository
2. Click on "Actions" tab
3. Enable workflows if disabled
4. The workflow will run automatically every 30 minutes

### Step 5: Manual Testing

To test immediately:
1. Go to Actions tab
2. Select "ETF Tracker - Telegram Updates"
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## 🌐 Trigger via Cron-Job.org

### Why Use External Cron?

GitHub Actions has a limitation where scheduled workflows may be delayed or disabled in inactive repositories. Using cron-job.org ensures reliable execution.

### Setup Steps:

1. **Create Personal Access Token (PAT)**
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Name: `ETF Tracker Workflow Trigger`
   - Expiration: Choose your preference
   - Select scope: `repo` (Full control of private repositories)
   - Generate and save the token

2. **Sign up at [cron-job.org](https://cron-job.org/)**

3. **Create New Cron Job**
   - Click "Create cronjob"
   - Title: `ETF Tracker - Every 30 min`
   - URL: 
     ```
     https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/dispatches
     ```
   - Schedule: `*/30 * * * *` (every 30 minutes)
   - Request Method: `POST`
   - Request Headers:
     ```
     Accept: application/vnd.github.v3+json
     Authorization: Bearer YOUR_GITHUB_PAT_TOKEN
     Content-Type: application/json
     ```
   - Request Body:
     ```json
     {
       "event_type": "etf-update"
     }
     ```

4. **Save and Enable**

### Alternative: Direct Workflow Dispatch

If you prefer using workflow_dispatch:

URL:
```
https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/actions/workflows/etf_tracker.yml/dispatches
```

Request Body:
```json
{
  "ref": "main"
}
```

## 📱 Sample Telegram Output

```
📊 ETF TRACKER UPDATE
⏰ 09-Feb-2026 02:30 PM IST
📈 Market Status: 🟢 OPEN

━━━━━━━━━━━━━━━━━━━━

🥇 TATA GOLD ETF (TATAGOLD)

💰 LTP: ₹5,234.50
📊 Open: ₹5,225.00
📈 High: ₹5,245.00
📉 Low: ₹5,220.00
🔄 Change: 9.50 (0.18%)
📦 Volume: 12.45K
🎯 iNAV: ₹5,230.25
📊 Premium/Discount: 0.08%

━━━━━━━━━━━━━━━━━━━━

🥈 TATA SILVER ETF (TATSILV)

💰 LTP: ₹72.45
📊 Open: ₹72.00
📈 High: ₹72.80
📉 Low: ₹71.95
🔄 Change: 0.45 (0.63%)
📦 Volume: 45.67K
🎯 iNAV: ₹72.40
📊 Premium/Discount: 0.07%

━━━━━━━━━━━━━━━━━━━━

🌍 INTERNATIONAL PRICES

💛 Gold: $2,045.30/oz
⚪ Silver: $23.45/oz

💵 FOREX
USD/INR: ₹83.15

━━━━━━━━━━━━━━━━━━━━

📌 KEY METRICS

🏆 Today's Winner: 🥈 Silver

Automated update every 30 minutes
```

## 🔧 Customization

### Change Update Frequency

Edit `.github/workflows/etf_tracker.yml`:

```yaml
schedule:
  - cron: '*/15 * * * *'  # Every 15 minutes
  - cron: '0 * * * *'     # Every hour
  - cron: '0 9-15 * * 1-5' # Every hour during market hours (Mon-Fri, 9am-3pm)
```

### Add More ETFs

Edit `etf_tracker.py` and add:

```python
# In the run() method:
bharat_bond_data = self.get_nse_data('BHARATBOND')
```

### Modify Message Format

Edit the `format_telegram_message()` function in `etf_tracker.py`

## 📊 iNAV Calculation Formula

```
iNAV = (International Spot Price in USD/oz ÷ 31.1035) × USD/INR × Units per ETF

For TATAGOLD/TATSILV: 1 unit = 1 gram

Premium/Discount % = ((Current LTP - iNAV) / iNAV) × 100
```

## 🐛 Troubleshooting

### Messages Not Sending?

1. Check GitHub Actions logs
2. Verify secrets are set correctly
3. Test bot token: `https://api.telegram.org/bot<TOKEN>/getMe`
4. Ensure bot is not blocked

### No NSE Data?

NSE may block requests. The script includes:
- User-Agent headers
- Session management
- Error handling

If issues persist, consider using alternative data sources.

### Rate Limiting?

- NSE: No official rate limit, but avoid excessive requests
- Gold API: Free tier has daily limits
- Telegram: 30 messages/second per bot

## 📝 Important Notes

1. **Market Hours**: NSE operates Mon-Fri, 9:15 AM - 3:30 PM IST
2. **Holidays**: Script runs on holidays too (NSE data will show last closing)
3. **Data Accuracy**: iNAV is indicative; actual NAV published EOD by AMC
4. **Free Tier Limits**: Gold API has daily request limits on free tier

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - feel free to use and modify

## ⚠️ Disclaimer

This tool is for informational purposes only. Not financial advice. Always verify data from official sources before making investment decisions.

## 🔗 Useful Links

- [NSE India](https://www.nseindia.com/)
- [MCX](https://www.mcxindia.com/)
- [Tata Mutual Fund](https://www.tatamutualfund.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

Made with ❤️ for ETF investors
