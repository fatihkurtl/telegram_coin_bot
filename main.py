import requests
import json
import asyncio
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler

bot_token = '6277255039:AAGdX4wW6SdRyr0PqrtBMv_r3M42PNHEzH8'

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
        bot.send_message(chat_id="-1001749926954", text=message)
    else:
        print('Hedef fiyat henuz gerceklesmedi.')
        message = f'BTC fiyati {last_price} dolar!'
        bot.send_message(chat_id="-1001749926954", text=message)

async def main():
    while True:
        await check_price()
        await asyncio.sleep(60)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Merhaba, ben BTC Fiyat Botu!")
    print('Bot baslatildi.')
    
    
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ben bir BTC fiyat botuyum. Hedef fiyat 28000 USD'dir. Fiyat hedefe ulastiginda kanala bildirim gonderilir.")
    print('Bot yardim edildi.')

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot durduruldu.")


def coin_price(update, context):
    coin = context.args[0].upper()
    response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT')
    data = json.loads(response.text)
    last_price = float(data['price'])
    message = f'{coin} fiyatı {last_price} USDT'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def error(update, context):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    updater = Updater(bot_token) #use_context=True
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('coinprice', coin_price))
    dp.add_error_handler(error)

    updater.start_polling()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
    


# how this project github push step by step
# git add .
# git commit -m "message"
# git push origin master
# bu kadar mı? -- fatih
# evet -- copilot