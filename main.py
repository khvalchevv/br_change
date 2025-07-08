from telethon import TelegramClient
import requests
import time

# --- Налаштування ---
API_ID = 22056618
API_HASH = 'db2bf3b16f1788d38091014befe31c0d'
SESSION_NAME = 'mexc_price_alert'

CHAT_ID = -1002604238211  
THREAD_ID = 11733 

MEXC_SYMBOL = 'BR_USDT'
THRESHOLD = 0.005         
INTERVAL = 5          

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

def get_futures_price(symbol):
    url = f'https://contract.mexc.com/api/v1/contract/ticker?symbol={symbol}'
    r = requests.get(url)
    data = r.json()
    return float(data['data']['lastPrice'])

async def main():
    await client.start()
    last_price = get_futures_price(MEXC_SYMBOL)
    print(f"Стартова ціна: {last_price}")

    while True:
        try:
            time.sleep(INTERVAL)
            current_price = get_futures_price(MEXC_SYMBOL)
            change = abs(current_price - last_price) / last_price

            if change >= THRESHOLD:
                direction = "📈" if current_price > last_price else "📉"
                msg = f"{direction} {MEXC_SYMBOL} змінився на {change*100:.2f}%: {current_price:.6f} USDT"
                await client.send_message(entity=CHAT_ID, message=msg, thread_id=THREAD_ID)
                last_price = current_price
        except Exception as e:
            print("⚠️ Помилка:", e)
            time.sleep(5)

with client:
    client.loop.run_until_complete(main())
