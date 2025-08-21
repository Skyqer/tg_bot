from dotenv import load_dotenv
import os

load_dotenv()

# Get token with validation
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in .env file")

MONOBANK_API_URL = "https://api.monobank.ua/bank/currency"

CRYPTO_SYMBOLS = {
    'Bitcoin': '₿ BTC',
    'Ethereum': 'Ξ ETH',
    'Solana': '◎ SOL',
    'Toncoin': '💎 TON'  # Fixed TON name
}

CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'UAH': '₴'
}
