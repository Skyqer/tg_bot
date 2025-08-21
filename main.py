import sys
import telebot
from config import BOT_TOKEN, CRYPTO_SYMBOLS, CURRENCY_SYMBOLS
from utils import get_change_emoji, format_price
from api_client import get_crypto_prices, get_exchange_rates

try:
    bot = telebot.TeleBot(BOT_TOKEN)
except Exception as e:
    print(f"Error initializing bot: {e}")
    sys.exit(1)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "Welcome! Use /help to see available commands."
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
🤖 *Available Commands*:

/prices - View cryptocurrency prices
/exchange - View UAH exchange rates
/help - Show this help message

_Bot updates data in real-time from CoinGecko and Monobank APIs._
"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['prices'])
def send_prices(message):
    prices = get_crypto_prices()
    if prices:
        response = "💹 *CRYPTO PRICES*\n\n"
        
        for crypto, data in prices.items():
            change_24h = data['change_24h']
            change_7d = data['change_7d']
            
            market_cap = data['market_cap']
            if market_cap >= 1e9:
                market_cap_str = f"{market_cap/1e9:.1f}B"
            else:
                market_cap_str = f"{market_cap/1e6:.1f}M"

            response += f"*{CRYPTO_SYMBOLS.get(crypto, crypto)}*\n"
            response += f"└ {CURRENCY_SYMBOLS['USD']}{format_price(data['USD'])} | {CURRENCY_SYMBOLS['UAH']}{format_price(data['UAH'])}\n"
            response += f"├ 24h: {change_24h:+.2f}% {get_change_emoji(change_24h)}\n"
            response += f"├ 7d:  {change_7d:+.2f}% {get_change_emoji(change_7d)}\n"
            response += f"└ MCap: {CURRENCY_SYMBOLS['USD']}{market_cap_str}\n\n"

        response += "⚡️ _Updated just now_ \n Use /help for commands."
        bot.reply_to(message, response, parse_mode='Markdown')
    else:
        bot.reply_to(message, "⚠️ *Error*: Could not fetch prices. Try again later.", parse_mode='Markdown')

@bot.message_handler(commands=['exchange'])
def send_exchange_rates(message):
    rates = get_exchange_rates()
    if rates:
        response = "💱 *EXCHANGE RATES*\n\n"
        
        for currency, rate in rates.items():
            symbol = CURRENCY_SYMBOLS.get(currency, currency)
            response += f"*{symbol} {currency}*\n"
            response += f"├ Buy:  {CURRENCY_SYMBOLS['UAH']}{rate['buy']:.2f}\n"
            response += f"└ Sell: {CURRENCY_SYMBOLS['UAH']}{rate['sell']:.2f}\n\n"
        
        response += "⚡️ _Monobank rates_"
        bot.reply_to(message, response, parse_mode='Markdown')
    else:
        bot.reply_to(message, "⚠️ *Error*: Could not fetch exchange rates. Try again later.", parse_mode='Markdown')

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling(none_stop=True)
