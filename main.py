import configparser
import logging
from html import escape

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from flask import Flask, request
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters


# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Set up logging
root = logging.getLogger()
root.setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))

welcome_message = '柳柳 NUMBER ONE !!!\n' \
                  '歡迎加入柳柳反指女神教！\n' \
                  '【 Grenade手榴彈 】'
 

# Inline keyborad button
reply_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton('Grenade粉專', url = 'https://www.facebook.com/Grenade2019/?fref=gs&dti=293728114864307&hc_location=group_dialog'),
    InlineKeyboardButton('Grenade社團', url = 'https://www.facebook.com/groups/Blockchainintw/'),
    InlineKeyboardButton('Instagram', url = 'https://www.instagram.com/grenade_2019/')]])


@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'


def start_handler(bot, update):
    """Send a message when the command /start is issued."""
    # update.message.reply_text("歡迎加入柳柳反指女神教！")

    # 需要有4個參數值 1.聊天室的id 2.發送訊息的標題 3. 回覆訊息的id, 4 回覆的內容
    """
    bot.send_message(update.message.chat.id, 'Grenade手榴彈', reply_to_message_id = update.message.message_id,
                     reply_markup = reply_markup)
    """
    update.message.reply_text(welcome_message, reply_markup=reply_markup)

    # print out log info
    logging.info('[start_handler][chat id]: %s' % update.message.chat.id)
    logging.info('[start_handler][reply_to_message_id]: %s' % update.message.message_id)
    logging.info('[start_handler][reply_markup]: %s' % reply_markup)   



def welcome(bot, update):
    """ Welcome a user to the group """

    logger.info('%s joined the group'
                 % (escape(update.message.new_chat_member.first_name)))

    # Pull the custom message for this chat from the database
    text = '歡迎加入柳柳反指女神教！'

    # Replace placeholders and send message
    """
    text = text.replace('$username',
                        update.message.new_chat_member.username)
    """
    bot.sendMessage(update.message.chat.id, text=text)
    # update.message.reply_text(text)



# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(CommandHandler('start', start_handler))  
# dispatcher.add_handler(welcome)

if __name__ == "__main__":
    # Running server
    app.run(debug=True)