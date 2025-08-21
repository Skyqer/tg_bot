import requests
from datetime import datetime, timedelta
from config import MONOBANK_API_URL

last_mono_request_time = None
cached_exchange_rates = None

def get_exchange_rates():
    global last_mono_request_time, cached_exchange_rates
    
    if last_mono_request_time and datetime.now() - last_mono_request_time < timedelta(seconds=60):
        return cached_exchange_rates
        
    try:
        response = requests.get(MONOBANK_API_URL)
        response.raise_for_status()
        rates = response.json()
        
        last_mono_request_time = datetime.now()
        
        exchange_rates = {}
        for rate in rates:
            if rate['currencyCodeA'] == 840 and rate['currencyCodeB'] == 980:
                exchange_rates['USD'] = {
                    'buy': rate['rateBuy'],
                    'sell': rate['rateSell']
                }
            elif rate['currencyCodeA'] == 978 and rate['currencyCodeB'] == 980:
                exchange_rates['EUR'] = {
                    'buy': rate['rateBuy'],
                    'sell': rate['rateSell']
                }
        
        cached_exchange_rates = exchange_rates
        return exchange_rates
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return None

def get_crypto_prices():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'ids': 'bitcoin,ethereum,solana,the-open-network',
        'order': 'market_cap_desc',
        'sparkline': 'false',
        'price_change_percentage': '24h,7d'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        prices = {}
        exchange_rates = get_exchange_rates()
        uah_rate = exchange_rates['USD']['buy'] if exchange_rates else 37.5
        
        for coin in data:
            name = 'Toncoin' if coin['id'] == 'the-open-network' else coin['name']
            uah_price = float(coin['current_price']) * uah_rate
            
            prices[name] = {
                'USD': coin['current_price'],
                'UAH': uah_price,
                'change_24h': coin['price_change_percentage_24h'] or 0,
                'change_7d': coin['price_change_percentage_7d_in_currency'] or 0,
                'market_cap': coin['market_cap'],
                'symbol': coin['symbol'].upper()
            }
        return prices
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None
