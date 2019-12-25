import os
from telegram.ext import Updater, CommandHandler
import pokepy
from modules import Type, Pic
import logging
START_TEXT = 'Hey! Pokedex here. Type /help to get list of commands'
ABOUT_TEXT = 'Bot made by Abhay Kshatriya (vegeto1806 on Telegram).\nThe source is available at https://github.com/kshatriya-abhay/pokebot'
HELP_TEXT = """
List of available commands:
/help - Get this list
/about - About the bot
/type - Get a Pokemon's type(s) and type weaknesses
/pic - Get a Pokemon's sprite
"""

poke_client = pokepy.V2Client(cache='in_disk', cache_location=(os.environ['HOME']+'/.cache'))

def start(update, context):
    update.message.reply_text(text = START_TEXT)

def about(update, context):
    update.message.reply_text(text = ABOUT_TEXT)

def get_help(update, context):
    update.message.reply_text(HELP_TEXT)

def get_type(update, context):
	if len(context.args) >= 1:
		query = '-'.join(context.args)
		response = ''
		response = Type.fetch_type(poke_client, query)
		update.message.reply_text(response)
	else:
		update.message.reply_text("Usage: /type Pikachu")

def get_pic(update, context):
	if len(context.args) >= 1:
		query = '-'.join(context.args)
		flag, response, pic_title = Pic.fetch_pic(poke_client, query)
		if flag:
			context.bot.send_photo(chat_id=update.effective_chat.id, photo=response, caption=pic_title, reply_to_message_id=update.effective_message.message_id)
			pass
		else:
			update.message.reply_text(response)
	else:
		update.message.reply_text("Usage: /pic Pikachu")

TOKEN_STRING = open('API_TOKEN','r').read().replace('\n','')
updater = Updater(TOKEN_STRING, use_context=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(CommandHandler('help', get_help))
updater.dispatcher.add_handler(CommandHandler('type', get_type))
updater.dispatcher.add_handler(CommandHandler('pic', get_pic))


updater.start_polling()
updater.idle()
