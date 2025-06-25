import os
import requests
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

def get_crypto_price(symbol: str) -> str:
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
        response = requests.get(url)
        response.raise_for_status()
        price = response.json()["price"]
        return f"{symbol.upper()}: **${price}**"
    except Exception as e:
        return f"Couldn't fetch {symbol.upper()}: {e}"

def get_top_10_prices() -> str:
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        top_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'SOLUSDT', 'TRXUSDT', 'DOTUSDT', 'MATICUSDT']
        prices = [get_crypto_price(symbol) for symbol in top_symbols]
        return "\n".join(prices)
    except Exception as e:
        return f"Couldn't fetch top 10 prices: {e}"

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.strip().lower()

    if "top 10" in user_input:
        result = get_top_10_prices()
    elif "who created" in user_input or "made you" in user_input or "creator" in user_input:
        result = "😄 I was created by **Abdul Salam**!"
    elif any(symbol in user_input.upper() for symbol in ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'TRX', 'DOT', 'MATIC']):
        cleaned = user_input.replace("price", "").strip().upper()
        result = get_crypto_price(cleaned)
    else:
        result = "❌ I can only help with cryptocurrency prices. Please ask something like `BTCUSDT`, `top 10`, or `who created you`."

    await cl.Message(content=result).send()
