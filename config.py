# Configuration for ETF Tracker

# ETF Configuration
ETFS = {
    'TATAGOLD': {
        'name': 'Tata Gold ETF',
        'symbol': 'TATAGOLD',
        'commodity': 'gold',
        'units_per_etf': 1,  # 1 unit = 1 gram
        'icon': '🥇'
    },
    'TATSILV': {
        'name': 'Tata Silver ETF',
        'symbol': 'TATSILV',
        'commodity': 'silver',
        'units_per_etf': 1,  # 1 unit = 1 gram
        'icon': '🥈'
    }
}

# Market Configuration
MARKET_CONFIG = {
    'timezone': 'Asia/Kolkata',
    'market_open_time': '09:15',
    'market_close_time': '15:30',
    'weekdays_only': True
}

# API Configuration
API_CONFIG = {
    'nse_base_url': 'https://www.nseindia.com',
    'forex_api_url': 'https://api.exchangerate-api.com/v4/latest/USD',
    'gold_spot_url': 'https://api.metals.live/v1/spot/gold',
    'silver_spot_url': 'https://api.metals.live/v1/spot/silver',
    'timeout': 10
}

# Message Configuration
MESSAGE_CONFIG = {
    'show_volume': True,
    'show_inav': True,
    'show_premium_discount': True,
    'show_international_prices': True,
    'show_forex': True,
    'show_performance_comparison': True,
    'decimal_places': 2
}

# Alert Configuration (optional - for future enhancement)
ALERT_CONFIG = {
    'enable_price_alerts': False,
    'gold_price_threshold': 5000,  # Alert if gold crosses this price
    'silver_price_threshold': 70,   # Alert if silver crosses this price
    'premium_threshold': 1.0,       # Alert if premium/discount exceeds 1%
}
