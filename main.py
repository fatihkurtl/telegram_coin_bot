import requests
import json
import asyncio
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler
import matplotlib.pyplot as plt
from datetime import datetime

bot_token = 'BOT_TOKEN'

bot = telegram.Bot(token=bot_token)
url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
target_price = 28000

async def check_price():
    response = requests.get(url)
    data = json.loads(response.text)
    last_price = float(data['price'])
    print('current_price: ', last_price)

    if last_price >= target_price:
        message = f'BTC fiyati {last_price} dolara ulasti!'
        bot.send_message(chat_id="CHAT_ID", text=message)
    else:
        print('Hedef fiyat henuz gerceklesmedi.')
        message = f'BTC fiyati {last_price} dolar!'
        bot.send_message(chat_id="CHAT_ID", text=message)

async def main():
    while True:
        await check_price()
        await asyncio.sleep(3600)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Merhaba, ben BTC Fiyat Botu!")
    print('Bot baslatildi.')

    
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ben bir BTC fiyat botuyum. /start komutu ile beni baslatabilirsiniz. /stop komutu ile beni durdurabilirsiniz. /chart <coin> komutu ile BTC fiyat ve diger coinlerin grafigini gorebilirsiniz. /price <coin> komutu ile BTC ve diger coinlerin fiyatini gorebilirsiniz. /news komutu ile kripto piyasasindaki en guncel 5 haberi görebilirsimiz. /help komutu ile benden yardim isteyebilirsiniz.")
    print('Bot yardim edildi.')

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot durduruldu.")
    print('Bot durduruldu.')

def chart(update, context):
    coin = context.args[0].upper()
    response = requests.get(f'https://api.binance.com/api/v3/klines?symbol={coin}USDT&interval=1d&limit=7')
    if response.status_code != 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text='API Error: Invalid coin symbol or network error.')
        return
    data = json.loads(response.text)
    x = []
    y = []
    for candle in data:
        timestamp = candle[0]/1000
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        x.append(date)
        y.append(float(candle[4]))
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y)
    ax.set_title(f'{coin} fiyatı (USDT)', fontsize=14)
    ax.set_xlabel('Tarih', fontsize=12)
    ax.set_ylabel('Fiyat (USDT)', fontsize=12)
    ax.yaxis.set_major_formatter('{:.2f}'.format)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('chart.png')
    plt.clf()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('chart.png', 'rb'))

def coin_price(update, context):
    coin = context.args[0].upper()
    response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT')
    data = json.loads(response.text)
    last_price = float(data['price'])
    message = f'{coin} fiyatı {last_price} USDT'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def crypto_news(update, context):
    url = 'https://api.coingecko.com/api/v3/news'
    response = requests.get(url)
    if response.status_code != 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text='API Error: Network error.')
        return
    data = response.json()
    for article in data['data'][:5]:
        title = article['title']
        description = article['description']
        url = article['url']
        message = f"{title}\n\n{description}\n\n{url}"
        bot.send_message(chat_id=update.effective_chat.id, text=message)


def error(update, context):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    updater = Updater(bot_token) #use_context=True
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('price', coin_price))
    dp.add_handler(CommandHandler('news', crypto_news))
    dp.add_handler(CommandHandler('chart', chart))
    dp.add_error_handler(error)

    updater.start_polling()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()