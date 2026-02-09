import requests
import json
from datetime import datetime
import pytz
import os

class ETFTracker:
    def __init__(self):
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        self.ist = pytz.timezone('Asia/Kolkata')
        
    def get_mcx_prices(self):
        """Fetch current MCX Gold and Silver prices"""
        try:
            # MCX Gold (per 10 grams) and Silver (per kg)
            # Using alternative API since direct MCX might need authentication
            response = requests.get('https://www.goldapi.io/api/XAU/INR', 
                                  headers={'x-access-token': os.environ.get('GOLD_API_KEY', '')},
                                  timeout=10)
            
            # Fallback to web scraping or alternative source
            mcx_data = {
                'gold_mcx': None,  # Per 10 grams
                'silver_mcx': None,  # Per kg
                'timestamp': datetime.now(self.ist).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Try NSE India API for international prices
            try:
                # Gold spot price in USD
                gold_usd_response = requests.get('https://api.metals.live/v1/spot/gold', timeout=10)
                if gold_usd_response.status_code == 200:
                    gold_data = gold_usd_response.json()
                    mcx_data['gold_usd_oz'] = gold_data.get('price')
                
                # Silver spot price in USD
                silver_usd_response = requests.get('https://api.metals.live/v1/spot/silver', timeout=10)
                if silver_usd_response.status_code == 200:
                    silver_data = silver_usd_response.json()
                    mcx_data['silver_usd_oz'] = silver_data.get('price')
            except:
                pass
            
            return mcx_data
        except Exception as e:
            print(f"Error fetching MCX prices: {e}")
            return {'error': str(e)}
    
    def get_forex_rates(self):
        """Fetch USD/INR exchange rate"""
        try:
            # Using exchangerate-api.com (free tier)
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'usd_inr': data['rates'].get('INR'),
                    'timestamp': data.get('time_last_updated')
                }
            return None
        except Exception as e:
            print(f"Error fetching forex rates: {e}")
            return None
    
    def get_nse_data(self, symbol):
        """Fetch NSE ETF data"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            # NSE API endpoint for ETF quotes
            url = f'https://www.nseindia.com/api/quote-equity?symbol={symbol}'
            
            session = requests.Session()
            session.get('https://www.nseindia.com', headers=headers, timeout=10)
            
            response = session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                price_info = data.get('priceInfo', {})
                
                return {
                    'symbol': symbol,
                    'ltp': price_info.get('lastPrice'),
                    'open': price_info.get('open'),
                    'high': price_info.get('intraDayHighLow', {}).get('max'),
                    'low': price_info.get('intraDayHighLow', {}).get('min'),
                    'close': price_info.get('close'),
                    'change': price_info.get('change'),
                    'pChange': price_info.get('pChange'),
                    'volume': data.get('marketDeptOrderBook', {}).get('totalTradedVolume'),
                    'value': data.get('marketDeptOrderBook', {}).get('totalTradedValue'),
                    'timestamp': datetime.now(self.ist).strftime('%Y-%m-%d %H:%M:%S')
                }
        except Exception as e:
            print(f"Error fetching NSE data for {symbol}: {e}")
            return None
    
    def calculate_inav(self, symbol, commodity_price_usd, usd_inr, units_per_etf):
        """
        Calculate indicative NAV (iNAV)
        
        For Gold ETF: 1 unit = 1 gram of gold
        For Silver ETF: 1 unit = 1 gram of silver
        
        iNAV = (Commodity Price in USD per oz / 31.1035) * USD/INR
        """
        try:
            if commodity_price_usd and usd_inr:
                # Convert from USD per troy oz to INR per gram
                price_per_gram_inr = (commodity_price_usd / 31.1035) * usd_inr
                inav = price_per_gram_inr * units_per_etf
                return round(inav, 2)
            return None
        except Exception as e:
            print(f"Error calculating iNAV: {e}")
            return None
    
    def is_market_open(self):
        """Check if Indian stock market is open"""
        now = datetime.now(self.ist)
        
        # Market hours: Monday-Friday, 9:15 AM - 3:30 PM IST
        if now.weekday() >= 5:  # Saturday or Sunday
            return False
        
        market_start = now.replace(hour=9, minute=15, second=0)
        market_end = now.replace(hour=15, minute=30, second=0)
        
        return market_start <= now <= market_end
    
    def format_telegram_message(self, gold_data, silver_data, mcx_data, forex_data):
        """Format comprehensive Telegram message"""
        now = datetime.now(self.ist)
        market_status = "🟢 OPEN" if self.is_market_open() else "🔴 CLOSED"
        
        message = f"""
📊 *ETF TRACKER UPDATE*
⏰ {now.strftime('%d-%b-%Y %I:%M %p IST')}
📈 Market Status: {market_status}

━━━━━━━━━━━━━━━━━━━━

🥇 *TATA GOLD ETF (TATAGOLD)*
"""
        
        if gold_data:
            message += f"""
💰 LTP: ₹{gold_data.get('ltp', 'N/A')}
📊 Open: ₹{gold_data.get('open', 'N/A')}
📈 High: ₹{gold_data.get('high', 'N/A')}
📉 Low: ₹{gold_data.get('low', 'N/A')}
🔄 Change: {gold_data.get('change', 'N/A')} ({gold_data.get('pChange', 'N/A')}%)
📦 Volume: {self.format_number(gold_data.get('volume', 0))}
"""
            
            # Calculate iNAV for Gold
            if mcx_data.get('gold_usd_oz') and forex_data:
                gold_inav = self.calculate_inav('TATAGOLD', mcx_data['gold_usd_oz'], 
                                               forex_data['usd_inr'], 1)
                if gold_inav:
                    premium_discount = ((gold_data.get('ltp', 0) - gold_inav) / gold_inav * 100) if gold_inav else 0
                    message += f"""
🎯 iNAV: ₹{gold_inav}
📊 Premium/Discount: {premium_discount:.2f}%
"""
        
        message += f"""
━━━━━━━━━━━━━━━━━━━━

🥈 *TATA SILVER ETF (TATSILV)*
"""
        
        if silver_data:
            message += f"""
💰 LTP: ₹{silver_data.get('ltp', 'N/A')}
📊 Open: ₹{silver_data.get('open', 'N/A')}
📈 High: ₹{silver_data.get('high', 'N/A')}
📉 Low: ₹{silver_data.get('low', 'N/A')}
🔄 Change: {silver_data.get('change', 'N/A')} ({silver_data.get('pChange', 'N/A')}%)
📦 Volume: {self.format_number(silver_data.get('volume', 0))}
"""
            
            # Calculate iNAV for Silver
            if mcx_data.get('silver_usd_oz') and forex_data:
                silver_inav = self.calculate_inav('TATSILV', mcx_data['silver_usd_oz'], 
                                                 forex_data['usd_inr'], 1)
                if silver_inav:
                    premium_discount = ((silver_data.get('ltp', 0) - silver_inav) / silver_inav * 100) if silver_inav else 0
                    message += f"""
🎯 iNAV: ₹{silver_inav}
📊 Premium/Discount: {premium_discount:.2f}%
"""
        
        message += f"""
━━━━━━━━━━━━━━━━━━━━

🌍 *INTERNATIONAL PRICES*
"""
        
        if mcx_data.get('gold_usd_oz'):
            message += f"\n💛 Gold: ${mcx_data['gold_usd_oz']:.2f}/oz"
        
        if mcx_data.get('silver_usd_oz'):
            message += f"\n⚪ Silver: ${mcx_data['silver_usd_oz']:.2f}/oz"
        
        if forex_data:
            message += f"""

💵 *FOREX*
USD/INR: ₹{forex_data['usd_inr']:.2f}
"""
        
        message += f"""
━━━━━━━━━━━━━━━━━━━━

📌 *KEY METRICS*
"""
        
        # Performance comparison
        if gold_data and silver_data:
            gold_perf = gold_data.get('pChange', 0)
            silver_perf = silver_data.get('pChange', 0)
            
            winner = "🥇 Gold" if gold_perf > silver_perf else "🥈 Silver"
            message += f"\n🏆 Today's Winner: {winner}"
        
        message += "\n\n_Automated update every 30 minutes_"
        
        return message
    
    def format_number(self, num):
        """Format large numbers for readability"""
        try:
            num = float(num)
            if num >= 10000000:  # Crores
                return f"{num/10000000:.2f}Cr"
            elif num >= 100000:  # Lakhs
                return f"{num/100000:.2f}L"
            elif num >= 1000:  # Thousands
                return f"{num/1000:.2f}K"
            return f"{num:.0f}"
        except:
            return "N/A"
    
    def send_telegram_message(self, message):
        """Send message to Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("✅ Telegram message sent successfully")
                return True
            else:
                print(f"❌ Failed to send Telegram message: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error sending Telegram message: {e}")
            return False
    
    def run(self):
        """Main execution function"""
        print("🚀 Starting ETF Tracker...")
        
        # Fetch all data
        print("📡 Fetching NSE data...")
        gold_data = self.get_nse_data('TATAGOLD')
        silver_data = self.get_nse_data('TATSILV')
        
        print("📡 Fetching MCX/International prices...")
        mcx_data = self.get_mcx_prices()
        
        print("📡 Fetching Forex rates...")
        forex_data = self.get_forex_rates()
        
        # Format and send message
        print("📝 Formatting message...")
        message = self.format_telegram_message(gold_data, silver_data, mcx_data, forex_data)
        
        print("📤 Sending to Telegram...")
        self.send_telegram_message(message)
        
        print("✅ ETF Tracker completed!")

if __name__ == "__main__":
    tracker = ETFTracker()
    tracker.run()
