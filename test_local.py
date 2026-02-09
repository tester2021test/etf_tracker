#!/usr/bin/env python3
"""
Local testing script for ETF Tracker
Run this before pushing to GitHub to test functionality
"""

import os
import sys

def check_environment():
    """Check if required environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"  ❌ {var} is not set")
        else:
            print(f"  ✅ {var} is set")
    
    if missing_vars:
        print("\n⚠️  Missing environment variables. Set them with:")
        print(f"  export TELEGRAM_BOT_TOKEN='your_token_here'")
        print(f"  export TELEGRAM_CHAT_ID='your_chat_id_here'")
        return False
    
    return True

def test_imports():
    """Test if all required packages are installed"""
    print("\n🔍 Checking required packages...")
    
    try:
        import requests
        print("  ✅ requests")
    except ImportError:
        print("  ❌ requests - Run: pip install requests")
        return False
    
    try:
        import pytz
        print("  ✅ pytz")
    except ImportError:
        print("  ❌ pytz - Run: pip install pytz")
        return False
    
    return True

def test_telegram_connection():
    """Test Telegram bot connection"""
    print("\n🔍 Testing Telegram connection...")
    
    import requests
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{token}/getMe"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_name = data['result'].get('username')
                print(f"  ✅ Connected to bot: @{bot_name}")
                return True
            else:
                print(f"  ❌ Error: {data}")
                return False
        else:
            print(f"  ❌ HTTP {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Connection failed: {e}")
        return False

def test_api_connectivity():
    """Test external API connectivity"""
    print("\n🔍 Testing API connectivity...")
    
    import requests
    
    apis = {
        'Forex API': 'https://api.exchangerate-api.com/v4/latest/USD',
        'Gold Spot API': 'https://api.metals.live/v1/spot/gold',
        'Silver Spot API': 'https://api.metals.live/v1/spot/silver',
    }
    
    all_ok = True
    for name, url in apis.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"  ✅ {name}")
            else:
                print(f"  ⚠️  {name} - HTTP {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"  ❌ {name} - {str(e)[:50]}")
            all_ok = False
    
    return all_ok

def run_tracker_test():
    """Run the actual tracker script"""
    print("\n🚀 Running ETF Tracker...")
    print("=" * 50)
    
    try:
        from etf_tracker import ETFTracker
        
        tracker = ETFTracker()
        tracker.run()
        
        print("=" * 50)
        print("✅ Tracker completed successfully!")
        return True
    except Exception as e:
        print("=" * 50)
        print(f"❌ Tracker failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("="*50)
    print("ETF TRACKER - LOCAL TESTING")
    print("="*50)
    
    tests = [
        ("Environment Variables", check_environment),
        ("Package Imports", test_imports),
        ("Telegram Connection", test_telegram_connection),
        ("API Connectivity", test_api_connectivity),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        if not test_func():
            all_passed = False
    
    if not all_passed:
        print("\n❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)
    
    print("\n✅ All preliminary tests passed!")
    
    # Ask user if they want to run the actual tracker
    print("\n" + "="*50)
    response = input("Do you want to run the tracker and send a test message? (y/n): ")
    
    if response.lower() == 'y':
        if run_tracker_test():
            print("\n🎉 All tests passed! You're ready to push to GitHub.")
        else:
            print("\n⚠️  Tracker test failed. Check the errors above.")
            sys.exit(1)
    else:
        print("\nTest skipped. Run the tracker manually when ready:")
        print("  python etf_tracker.py")

if __name__ == "__main__":
    main()
