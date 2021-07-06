import json
import time
import telebot
import threading
import concurrent.futures
import datetime
import pytz
import os

from dotenv import load_dotenv
from telebot import types, apihelper
from modules.scraper import WebScraper
from modules.reuters import Reuters
from modules.seekingAlpha import SeekingAlpha
from modules.utils.misc import write_json, check_strength, beautify_emoji, add_keyword, remove_keyword, display_keywords

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = telebot.TeleBot(token=BOT_TOKEN)
scraper = WebScraper()
seekingalpha = SeekingAlpha()
reuters = Reuters()
approvedList = ["ADMIN_IDS HERE"]

seleniumTimeout = False

@bot.message_handler(commands=['stock'], func=lambda message: message.chat.type == 'supergroup' and message.chat.id == int(CHAT_ID))
def send_random_stock(message):
    randomStock = scraper.random_stock()
    bot.send_message(message.chat.id, randomStock)


@bot.message_handler(commands =['analyse'], func=lambda message: message.chat.type == 'supergroup' and message.chat.id == int(CHAT_ID))
def analyse_stock(message):
    global seleniumTimeout

    if seleniumTimeout is True:
        return bot.reply_to(message, '*Error* - Command is on cooldown', parse_mode='Markdown')     # Checks if command is on cooldown
    
    messageLength = len(message.text.split())
    if messageLength != 2:   # Ensure that correct parameters are entered
        return bot.reply_to(message, 'This command only accepts _*one*_ parameter', parse_mode='MarkdownV2')
    else:
        seleniumTimeout = True
        timeFrameList = ['1Min', '5Mins', '15Mins', '1Hour', '4Hours', '1Day', '1Week', '1Month']
        markup = types.InlineKeyboardMarkup()

        # Populate timeframe buttons
        for x in range(0, len(timeFrameList), 2):
            markup.add(types.InlineKeyboardButton(text=timeFrameList[x], callback_data=f'Timeframe - {timeFrameList[x]}'), types.InlineKeyboardButton(text=timeFrameList[x + 1], callback_data=f'Timeframe - {timeFrameList[x + 1]}'))
        
        # Creates a cancel button
        markup.add(types.InlineKeyboardButton(text='❌', callback_data='Delete'))
        text = f'''
*Stock Symbol* - {message.text.split()[-1].upper()}
Select timeframe for analysis:
        '''
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)
        seleniumTimeout = False


@bot.message_handler(commands=['add'], func=lambda message: message.chat.type == 'supergroup' and message.from_user.id in approvedList and message.chat.id == int(CHAT_ID))
def add(message):
    if message.from_user.id not in [x.user.id for x in bot.get_chat_administrators(CHAT_ID)]:
        return bot.reply_to(message, 'You do not have access to this command', parse_mode='Markdown')

    # messageLength = len(message.text.split())
    # if messageLength != 2:   # Ensure that correct parameters are entered
    #     return bot.reply_to(message, 'This command only accepts _*one*_ parameter', parse_mode='MarkdownV2')
    
    keyword = message.text[5:]
    add_keyword(keyword)
    text = f'✅ *Keyword* : _{keyword}_ has been added from watchlist'

    bot.reply_to(message, text, parse_mode='Markdown')


@bot.message_handler(commands=['remove'], func=lambda message: message.chat.type == 'supergroup' and message.from_user.id in approvedList and message.chat.id == int(CHAT_ID))
def remove(message):
    if message.from_user.id not in [x.user.id for x in bot.get_chat_administrators(CHAT_ID)]:
        return bot.reply_to(message, 'You do not have access to this command', parse_mode='Markdown')

    # messageLength = len(message.text.split())
    # if messageLength > 2:   # Ensure that correct parameters are entered
    #     return bot.reply_to(message, 'This command only accepts _*one*_ parameter', parse_mode='MarkdownV2')

    original = message.text[8::]
    keyword = message.text.split()[1:]
    updatedKeyword = '(.?)'.join(keyword)
    try:    # Error catch for keywords that does not exist
        remove_keyword(updatedKeyword)
        text = f'*Keyword* : _{original}_ has been removed from watchlist'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    except:
        text = f'*Keyword* : _{original}_ does not exist in watchlist'
        bot.reply_to(message, text, parse_mode='Markdown')


@bot.message_handler(commands=['display'], func=lambda message: message.chat.type == 'supergroup' and message.from_user.id in approvedList and message.chat.id == int(CHAT_ID))
def display(message):
    if message.from_user.id not in [x.user.id for x in bot.get_chat_administrators(CHAT_ID)]:
        return bot.reply_to(message, 'You do not have access to this command', parse_mode='Markdown')

    text = f'*Current Watchlist*: {display_keywords()}'
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands =['news'], func=lambda message: message.chat.type == 'supergroup' and message.chat.id == int(CHAT_ID))
def news(message):
    global seleniumTimeout

    if seleniumTimeout is True:
        return bot.reply_to(message, '*Error* - Command is on cooldown', parse_mode='Markdown')     # Checks if command is on cooldown
    
    messageLength = len(message.text.split(' '))
    if messageLength != 3:   # Ensure that correct parameters are entered
        return bot.reply_to(message, 'Command usage: _*/news <market> <stockSymbol>*_', parse_mode='MarkdownV2')
    elif message.text.split(' ')[1].lower() not in ['sg', 'us']:   # Check if correct market is input
        return bot.reply_to(message, 'Markets avaiable: _*SG/US*_', parse_mode='MarkdownV2')

    botMessage = bot.send_message(message.chat.id, text='_Loading_', parse_mode='Markdown')

    symbol = message.text.split()[2]
    data = {}
    if message.text.split(' ')[1].lower() == 'us':
        seleniumTimeout = True
        data = scraper.retrieve_us_news(symbol)
        seleniumTimeout = False
    elif message.text.split(' ')[1].lower() == 'sg':
        data = scraper.retrieve_sg_news(symbol)

    if (data == 'Error'):
        text = f'*Error* - {symbol} does not exist.'
        return bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        text = ''
        emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        index = 0
        for key in data.keys():
            for x in range(0, len(data[key]), 3):
                text += f"""
{emoji[index]} {data[key][x]}
🔗: {data[key][x + 1]}
📅: _{key} {data[key][x + 2]}_
                """
                index += 1
        try:
            bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=botMessage.message_id, parse_mode='Markdown', disable_web_page_preview=True)
        except apihelper.ApiTelegramException:     # In case link contains double _ characters
            bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=botMessage.message_id, disable_web_page_preview=True)
        except:
            bot.edit_message_text(text='*Error* - Not able to retrieve data. Try again later.', chat_id=message.chat.id, message_id=message.message_id, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda query: True)
def handle_query(query):
    global seleniumTimeout

    if (query.data.startswith('Timeframe')):
        timeFrame = query.data
        valueFromCallBack = timeFrame.split()[2]
        bot.answer_callback_query(callback_query_id = query.id, show_alert = True)
        symbol = query.message.text.split()[-5]

        bot.edit_message_text(text='_Loading_', chat_id=query.message.chat.id, message_id=query.message.message_id, parse_mode='Markdown')
        seleniumTimeout = True
        data = scraper.analyse_stock(symbol, valueFromCallBack)

        if (data == 'Error'):   # Error retrieving data
            return bot.edit_message_text(text='*Error* - Not able to retrieve data. Try again later.', chat_id=query.message.chat.id, message_id=query.message.message_id, parse_mode='Markdown')
        
        text = f"""
📋 *Stock Name*: {data[0]}
💵 *Current Price*: {data[1]}
📊 *Price Change*: {data[2]}
📈 *P/E Ratio*: {data[3]}

⚖️ *Analysis* (Timeframe - {valueFromCallBack})
> *Relative Strength Index*: {beautify_emoji(data[5])} ({data[4]}%)
> *Moving Average*: {beautify_emoji(data[7])} ({check_strength(data[6])})
    """

        try:
            bot.edit_message_text(text=text, chat_id=query.message.chat.id, message_id=query.message.message_id, parse_mode='Markdown')
        except:
            bot.send_message(query.message.chat.id, text=text, parse_mode='Markdown')
        
        seleniumTimeout = False
    
    elif (query.data.startswith('Delete')):
        bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)

# Ensure all previous requests are erased
def clear_updates():
    latestUpdates = bot.get_updates()
    if latestUpdates:
        latestUpdateID = latestUpdates[-1].update_id + 1
        bot.get_updates(offset=latestUpdateID)
        print('Erased all pending requests')
    else:
        print('No updates')

# Thread 1 function
def bot_polling():
    try:
        print('---WebScraper is Online---')
        clear_updates()
        bot.polling(none_stop=True)
    except Exception as e:
        write_json(e)

# Thread 2 function
def send_reuters_scraped_links():
    while True:
        reutersLinks = reuters.analyse_url()

        if len(reuters.sentLinks) > 30:     # Resets the memory log of links
            reuters.sentLinks.clear()
        
        if (reutersLinks):
            for link in reutersLinks:
                text = f'*Keyword Found* - {reutersLinks[link]}\n {link}'
                bot.send_message(chat_id=CHAT_ID, text=text, disable_web_page_preview=True)
            print('---Analysis of Links Completed---')
        else:
            print('---No Links Found---')
        
        minute = 60
        time.sleep(10*minute)

# Thread 3 function
def send_seekingalpha_scraped_links():
    while True:
        seekingalphaLinks = seekingalpha.analyse_url()

        if len(seekingalpha.sentLinks) > 30:    # Resets the memory log of links
            seekingalpha.sentLinks.clear()
        
        if (seekingalphaLinks):
            for link in seekingalphaLinks:
                text = f'*Keyword Found* - {seekingalphaLinks[link]}\n {link}'
                bot.send_message(chat_id=CHAT_ID, text=text, disable_web_page_preview=True)
            print('---Analysis of Links Completed---')
        else:
            print('---No Links Found---')

        minute = 60
        time.sleep(10*minute)


telegram = threading.Thread(target=bot_polling)
reutersNews = threading.Thread(target=send_reuters_scraped_links)
seekingalphaNews = threading.Thread(target=send_seekingalpha_scraped_links)

if __name__ == "__main__":
    try:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        telegram.start()
        reutersNews.start()
        seekingalphaNews.start()
    except Exception as e:
        write_json(repr(e))
