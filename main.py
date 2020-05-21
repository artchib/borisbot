from telegram import Bot
from telegram import Update
from telegram.ext import Updater, CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram.ext import Filters
from config import TG_TOKEN
from logging import getLogger
from data_b.db import add_user
from data_b.db import get_karma
from data_b.db import update_karma
from data_b.db import isCreate
from data_b.db import init_db


logger = getLogger(__name__)


def do_start(update:Update, context=CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Приветствую! Я - бот Борис.\n'
             'Что бы узнать что я умею воспользуйтесь командой /help'
    )

def do_help(update: Update, context= CallbackContext):
    print('govno')
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Что бы поблагодарить участника группы, ответьте на его сообщение со знака + \n'
              'Что бы поднасрать участнику группы, ответьте на его сообщение со знака -'
    )

def do_text(update:Update, context=CallbackContext):
    chat_id = update.effective_chat.id
    message = update.message.text
    user_id_reply_from = update.message.reply_to_message.from_user.id
    if update.message.reply_to_message:
        if message.startswith('+'):
            if isCreate(user_id=user_id_reply_from):
                update_karma(user_id=user_id_reply_from, karma=get_karma(user_id=user_id_reply_from)+1)
            else:
                add_user(user_id=user_id_reply_from, karma=1)

            context.bot.send_message(
                chat_id=chat_id,
                text= f'{update.message.from_user.first_name} поблагодорил {update.message.reply_to_message.from_user.first_name}\n'
                       f'Карма {update.message.reply_to_message.from_user.first_name} = {get_karma(user_id=user_id_reply_from)}'
            )
        elif message.startswith('-'):
            if isCreate(user_id=user_id_reply_from):
                update_karma(user_id=user_id_reply_from, karma=get_karma(user_id=user_id_reply_from)-1)
            else:
                add_user(user_id=user_id_reply_from, karma=-1)

            context.bot.send_message(
                chat_id=chat_id,
                text= f'{update.message.from_user.first_name} поднасрал {update.message.reply_to_message.from_user.first_name}\n'
                       f'Карма {update.message.reply_to_message.from_user.first_name} = {get_karma(user_id=user_id_reply_from)}'
            )

    else:
        print('inside else isCreate')
        context.bot.send_message(
            chat_id=chat_id,
            text=f'Karma bez otveta',
        )




def main():
    logger.info("Запускаем бота...")
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )
    init_db()



    info = bot.getMe()
    logger.info(f'Bot info: {info}')


    start_handler = CommandHandler('start', do_start)
    help_handler = CommandHandler("help", do_help)
    text_handler = MessageHandler(Filters.text, do_text)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(text_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
