def get_change_emoji(change):
    if change > 5:
        return "🚀"
    elif change > 0:
        return "📈"
    elif change < -5:
        return "💔"
    elif change < 0:
        return "📉"
    return "➖"

def format_price(price):
    if price >= 1:
        return f"{price:,.2f}"
    return f"{price:.8f}"
