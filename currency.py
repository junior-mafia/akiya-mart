import locale
import requests
import os

URL = 'https://openexchangerates.org/api/latest.json'

def yen_to_usd(amount_yen, yen_per_usd):
    return amount_yen / yen_per_usd

def usd_to_yen(amount_usd, yen_per_usd):
    return amount_usd * yen_per_usd

# Assumes format like: 20万円
def undisplay_yen(amount: str):
    if '〜' in amount:
        amount = amount.split('〜')[1]
    
    if '※権利金含む' in amount:
        amount = amount.split('※権利金含む')[1]

    amount = amount.replace("万", "").replace("円", "").replace(",", "")
    try:
        amount = int(float(amount)) * 10000
    except:
        print(amount)
        raise "hiiii"
    return amount

def display_yen(amount: int):
    locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
    return locale.currency(amount, grouping=True)

def display_usd(amount: float):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(amount, grouping=True)[:-3]

def raw_japanese_price_to_usd_display(price: str, exchange_rate):
    price_yen = undisplay_yen(price)
    price_usd = yen_to_usd(price_yen, exchange_rate)
    return display_usd(price_usd)

def price_yen_to_usd_display(price_yen: int, exchange_rate):
    price_usd = yen_to_usd(price_yen, exchange_rate)
    return display_usd(price_usd)

def get_yen_per_usd():
    OPEN_EXCHANGE_RATES_API_KEY = os.environ['OPEN_EXCHANGE_RATES_API_KEY']
    base_currency = 'JPY'
    params = {
        'app_id': OPEN_EXCHANGE_RATES_API_KEY,
        'symbols': base_currency
    }
    response = requests.get(URL, params=params)
    return response.json()['rates']['JPY']
