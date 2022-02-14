import logging
import sys
from logging import StreamHandler

from django.core.management.base import BaseCommand
from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, Filters, MessageHandler, Updater
from telegram.ext.commandhandler import CommandHandler

from django_tg_bot.settings import BOT_TOKEN

from .utils.seacrh import get_addresses, get_count_response, save_db


def start(update, context):
    keyboard = [["Новый поиск", "История"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, one_time_keyboard=True, resize_keyboard=True
    )
    update.message.reply_text("Привет! Чем помочь?", reply_markup=reply_markup)
    return 1


def first(update, context):
    chat_id = update.message.chat_id
    if update.message.text == "Новый поиск":
        context.bot.send_message(
            chat_id=chat_id,
            text="Введите адрес поиска:",
        )
        return 2
    elif update.message.text == "История":
        message = get_count_response(chat_id)
        if not message:
            message = ["Записей не найдено"]
        context.bot.send_message(
            chat_id=chat_id,
            text=f"{''.join(message)}\n\nВернутся в меню /start",
        )
        return ConversationHandler.END
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=f"Что-то не понятное.\nДавайте начнем сначала /start",
        )
        return ConversationHandler.END


def second(update, context):
    query = update.message.text
    addresses = get_addresses(query)
    if addresses:
        save_db(query, addresses, update.message.chat_id)
    else:
        addresses = "В доступных зонах поиска не найден адрес."
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"{addresses}\n\nВернутся в меню /start",
    )
    return ConversationHandler.END


def again(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"Что-то не понятное.\nДавайте начнем сначала /start",
    )


class Command(BaseCommand):
    help = "Телеграмм-бот геокодера Яндекс.Карт"

    def handle(self, *args, **options):
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s, %(levelname)s, %(message)s, %(name)s",
        )
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = StreamHandler(stream=sys.stdout)
        logger.addHandler(handler)

        updater = Updater(token=BOT_TOKEN)

        updater.dispatcher.add_handler(
            ConversationHandler(
                entry_points=[CommandHandler("start", start)],
                states={
                    1: [MessageHandler(Filters.text, first)],
                    2: [MessageHandler(Filters.text, second)],
                },
                fallbacks=[],
            )
        )
        updater.dispatcher.add_handler(MessageHandler(Filters.text, again))
        updater.start_polling()
        updater.idle()
