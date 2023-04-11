import requests
import json
import asyncio
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot_token = '6277255039:AAGdX4wW6SdRyr0PqrtBMv_r3M42PNHEzH8'
bot = telegram.Bot(token=bot_token)

coins = {}

def set_coin(update, context):
    chat_id = update.effective_chat.id
    coin = context.args[0].upper()
    coins[chat_id] = coin
    bot.send_message(chat_id=chat_id, text=f"{coin} is set as the target coin!")

def cancel_coin(update, context):
    chat_id = update.effective_chat.id
    if chat_id in coins:
        del coins[chat_id]
    bot.send_message(chat_id=chat_id, text="Target coin is cancelled.")

def get_price(update, context):
    chat_id = update.effective_chat.id
    if chat_id in coins:
        coin = coins[chat_id]
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT'
        response = requests.get(url)
        data = json.loads(response.text)
        last_price = float(data['price'])
        message = f'Current {coin} price is {last_price} USDT.'
        bot.send_message(chat_id=chat_id, text=message)
    else:
        bot.send_message(chat_id=chat_id, text="Please set the target coin using /set_coin command first.")

def error(update, context):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('set_coin', set_coin))
    dp.add_handler(CommandHandler('cancel_coin', cancel_coin))
    dp.add_handler(CommandHandler('get_price', get_price))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

