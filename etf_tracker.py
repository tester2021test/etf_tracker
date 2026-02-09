import requests
import json
from datetime import datetime
import pytz
import os
import logging
import time
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etf_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def retry_with_backoff(max_retries=3, backoff_factor=2):
    """Decorator for retry logic with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...")
                    
                    if attempt == max_retries - 1:
                        logger.error(f"All {max_retries} attempts failed for {func.__name__}")
                        raise
                    
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator

class ETFTrackerEnhanced:
    def __init__(self):
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        self.ist = pytz.timezone('Asia/Kolkata')
        self.errors = []
        
        logger.info("ETF Tracker Enhanced initialized")
        
    def validate_price_data(self, data, symbol):
        """Validate price data for anomalies"""
        if not data or not data.get('ltp'):
            logger.warning(f"Invalid data structure for {symbol}")
            return False
        
        ltp = data.get('ltp', 0)
        
        # Check for reasonable price range
        if symbol == 'TATAGOLD':
            if not (3000 < ltp < 10000):
                logger.warning(f"Gold price {ltp} outside expected range (3000-10000)")
                return False
        elif symbol == 'TATSILV':
            if not (40 < ltp < 200):
                logger.warning(f"Silver price {ltp} outside expected range (40-200)")
                return False
        
        # Check for required fields
        required_fields = ['ltp', 'open', 'high', 'low']
        for field in required_fields:
            if field not in data or data[field] is None:
                logger.warning(f"Missing required field '{field}' for {symbol}")
                return False
        
        logger.info(f"Price data validated successfully for {symbol}: ₹{ltp}")
        return True
    
    @retry_with_backoff(max_retries=3)
    def get_mcx_prices(self):
        """Fetch current MCX Gold and Silver prices with retry"""
        logger.info("Fetching MCX/International prices...")
        
        try:
            mcx_data = {
                'gold_mcx': None,
                'silver_mcx': None,
                'timestamp': datetime.now(self.ist).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Try gold spot price
            try:
                gold_response = requests.get('https://api.metals.live/v1/spot/gold', timeout=10)
                if gold_response.status_code == 200:
                    gold_data = gold_response.json()
                    mcx_data['gold_usd_oz'] = gold_data.get('price')
                    logger.info(f"Gold spot: ${mcx_data['gold_usd_oz']}/oz")
            except Exception as e:
                logger.warning(f"Failed to fetch gold price: {e}")
            
            # Try silver spot price
            try:
                silver_response = requests.get('https://api.metals.live/v1/spot/silver', timeout=10)
                if silver_response.status_code == 200:
                    silver_data = silver_response.json()
                    mcx_data['silver_usd_oz'] = silver_data.get('price')
                    logger.info(f"Silver spot: ${mcx_data['silver_usd_oz']}/oz")
            except Exception as e:
                logger.warning(f"Failed to fetch silver price: {e}")
            
            return mcx_data
            
        except Exception as e:
            logger.error(f"Error in get_mcx_prices: {e}")
            self.errors.append(f"MCX Prices: {str(e)}")
            raise
    
    @retry_with_backoff(max_retries=3)
    def get_forex_rates(self):
        """Fetch USD/INR exchange rate with retry"""
        logger.info("Fetching forex rates...")
        
        try:
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=10)
            if response.status_code == 200:
                data = response.json()
                usd_inr = data['rates'].get('INR')
                logger.info(f"USD/INR: ₹{usd_inr}")
                return {
                    'usd_inr': usd_inr,
                    'timestamp': data.get('time_last_updated')
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching forex rates: {e}")
            self.errors.append(f"Forex: {str(e)}")
            raise
    
    @retry_with_backoff(max_retries=3)
    def get_nse_data(self, symbol):
        """Fetch NSE ETF data with retry"""
        logger.info(f"Fetching NSE data for {symbol}...")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            url = f'https://www.nseindia.com/api/quote-equity?symbol={symbol}'
            
            session = requests.Session()
            session.get('https://www.nseindia.com', headers=headers, timeout=10)
            
            response = session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                price_info = data.get('priceInfo', {})
                
                result = {
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
                
                # Validate data before returning
                if self.validate_price_data(result, symbol):
                    logger.info(f"Successfully fetched {symbol} data: LTP ₹{result['ltp']}")
                    return result
                else:
                    logger.error(f"Data validation failed for {symbol}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching NSE data for {symbol}: {e}")
            self.errors.append(f"NSE {symbol}: {str(e)}")
            raise
    
    def calculate_inav(self, symbol, commodity_price_usd, usd_inr, units_per_etf):
        """Calculate indicative NAV (iNAV)"""
        try:
            if commodity_price_usd and usd_inr:
                price_per_gram_inr = (commodity_price_usd / 31.1035) * usd_inr
                inav = price_per_gram_inr * units_per_etf
                logger.info(f"{symbol} iNAV calculated: ₹{inav:.2f}")
                return round(inav, 2)
            return None
        except Exception as e:
            logger.error(f"Error calculating iNAV for {symbol}: {e}")
            return None
    
    def is_market_open(self):
        """Check if Indian stock market is open"""
        now = datetime.now(self.ist)
        
        if now.weekday() >= 5:
            logger.info("Market closed: Weekend")
            return False
        
        market_start = now.replace(hour=9, minute=15, second=0)
        market_end = now.replace(hour=15, minute=30, second=0)
        
        is_open = market_start <= now <= market_end
        logger.info(f"Market status: {'OPEN' if is_open else 'CLOSED'}")
        return is_open
    
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
            
            if mcx_data.get('gold_usd_oz') and forex_data:
                gold_inav = self.calculate_inav('TATAGOLD', mcx_data['gold_usd_oz'], 
                                               forex_data['usd_inr'], 1)
                if gold_inav:
                    premium_discount = ((gold_data.get('ltp', 0) - gold_inav) / gold_inav * 100) if gold_inav else 0
                    message += f"""
🎯 iNAV: ₹{gold_inav}
📊 Premium/Discount: {premium_discount:.2f}%
"""
        else:
            message += "\n⚠️ Data unavailable\n"
        
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
            
            if mcx_data.get('silver_usd_oz') and forex_data:
                silver_inav = self.calculate_inav('TATSILV', mcx_data['silver_usd_oz'], 
                                                 forex_data['usd_inr'], 1)
                if silver_inav:
                    premium_discount = ((silver_data.get('ltp', 0) - silver_inav) / silver_inav * 100) if silver_inav else 0
                    message += f"""
🎯 iNAV: ₹{silver_inav}
📊 Premium/Discount: {premium_discount:.2f}%
"""
        else:
            message += "\n⚠️ Data unavailable\n"
        
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
        
        if gold_data and silver_data:
            gold_perf = gold_data.get('pChange', 0)
            silver_perf = silver_data.get('pChange', 0)
            
            winner = "🥇 Gold" if gold_perf > silver_perf else "🥈 Silver"
            message += f"\n🏆 Today's Winner: {winner}"
        
        # Add error summary if any
        if self.errors:
            message += f"\n\n⚠️ *Errors encountered:* {len(self.errors)}"
        
        message += "\n\n_Automated update every 30 minutes_"
        
        return message
    
    def format_number(self, num):
        """Format large numbers for readability"""
        try:
            num = float(num)
            if num >= 10000000:
                return f"{num/10000000:.2f}Cr"
            elif num >= 100000:
                return f"{num/100000:.2f}L"
            elif num >= 1000:
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
                logger.info("✅ Telegram message sent successfully")
                return True
            else:
                logger.error(f"Failed to send Telegram message: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def send_error_alert(self):
        """Send error notification if errors occurred"""
        if not self.errors:
            return
        
        error_message = f"""
⚠️ *ETF TRACKER - ERROR ALERT*

{len(self.errors)} error(s) occurred during last run:

"""
        for idx, error in enumerate(self.errors, 1):
            error_message += f"{idx}. {error}\n"
        
        error_message += f"""
Time: {datetime.now(self.ist).strftime('%d-%b-%Y %I:%M %p IST')}

Check GitHub Actions logs for details.
"""
        
        self.send_telegram_message(error_message)
        logger.info(f"Sent error alert with {len(self.errors)} errors")
    
    def get_health_status(self):
        """Get system health status"""
        health = {
            'timestamp': datetime.now(self.ist).isoformat(),
            'telegram': 'unknown',
            'nse': 'unknown',
            'forex': 'unknown',
            'commodities': 'unknown'
        }
        
        # Test Telegram
        try:
            test_url = f"https://api.telegram.org/bot{self.telegram_token}/getMe"
            response = requests.get(test_url, timeout=5)
            health['telegram'] = 'OK' if response.status_code == 200 else 'FAIL'
        except:
            health['telegram'] = 'FAIL'
        
        logger.info(f"Health check: {health}")
        return health
    
    def run(self):
        """Main execution function with enhanced error handling"""
        logger.info("="*50)
        logger.info("🚀 Starting ETF Tracker Enhanced...")
        logger.info("="*50)
        
        # Reset errors
        self.errors = []
        
        # Initialize variables
        gold_data = None
        silver_data = None
        mcx_data = None
        forex_data = None
        
        # Fetch all data with error handling
        try:
            logger.info("📡 Fetching NSE data...")
            gold_data = self.get_nse_data('TATAGOLD')
        except Exception as e:
            logger.error(f"Failed to fetch TATAGOLD data: {e}")
        
        try:
            silver_data = self.get_nse_data('TATSILV')
        except Exception as e:
            logger.error(f"Failed to fetch TATSILV data: {e}")
        
        try:
            logger.info("📡 Fetching MCX/International prices...")
            mcx_data = self.get_mcx_prices()
        except Exception as e:
            logger.error(f"Failed to fetch MCX data: {e}")
        
        try:
            logger.info("📡 Fetching Forex rates...")
            forex_data = self.get_forex_rates()
        except Exception as e:
            logger.error(f"Failed to fetch forex data: {e}")
        
        # Format and send message even with partial data
        logger.info("📝 Formatting message...")
        message = self.format_telegram_message(gold_data, silver_data, mcx_data, forex_data)
        
        logger.info("📤 Sending to Telegram...")
        self.send_telegram_message(message)
        
        # Send error alert if needed
        if self.errors:
            logger.warning(f"⚠️ Run completed with {len(self.errors)} errors")
            self.send_error_alert()
        else:
            logger.info("✅ ETF Tracker completed successfully!")
        
        logger.info("="*50)

if __name__ == "__main__":
    tracker = ETFTrackerEnhanced()
    tracker.run()
