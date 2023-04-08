import requests
import json
import time
import telegram
import asyncio
from telegram.ext import Updater, CommandHandler, MessageHandler

bot = telegram.Bot(token='6277255039:AAGdX4wW6SdRyr0PqrtBMv_r3M42PNHEzH8')

url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'

target_price = 28000

async def check_price():
    response = requests.get(url)
    data = json.loads(response.text)
    last_price = float(data['price'])
    print('current_price: ', last_price)
    
    if last_price >= target_price:
        message = f'BTC fiyati {last_price} dolara ulasti!'
        bot.send_message(chat_id="@conquerorl", text=message)
    else: 
        print('Hedef fiyat henuz gerceklesmedi.')
        message = f'BTC fiyati {last_price} dolar!'
        # await bot.send_message(chat_id="676668138", text=message)

async def main():
    while True:
        await check_price()
        time.sleep(60)
    
if __name__ == '__main__':
    asyncio.run(main())