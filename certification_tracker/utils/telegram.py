"""Telegram Bot implementation"""
import json
from pathlib import Path
from time import sleep

from telegram import Bot
from telegram.ext import Updater


class TelegramBot:
    """
    This class implements telegram bot that is used for sending updates to a telegram chat
    :attr:`bot` Telegram bot object
    :attr:`updater` Telegram updater object
    :attr:`chat` Telegram chat username or id
    """

    def __init__(self):
        """
        TelegramBot class constructor
        :param bot_token: Telegram Bot API access token
        :param chat: Telegram chat username or id that will be used to send updates to
        """
        config_path = Path(__package__).absolute().parent
        with open(f"{config_path}/telegram_config.json", 'r') as config:
            self.config: dict = json.load(config)
        self.bot: Bot = Bot(token=self.config.get('tg_bot_token'))
        self.updater = Updater(bot=self.bot, use_context=True)
        chat = self.config.get('tg_chat')
        self.chat = int(chat) if chat.startswith('-') else f"{self.config.get('tg_chat')}"

    def send_telegram_message(self, message: str):
        """
        Send a message to Telegram chat
        :param message: A string of the update message to be sent
        :return:
        """
        message = f"{message}\n{self.chat}"
        self.updater.bot.send_message(
            chat_id=self.chat, text=message,
            parse_mode='Markdown',
            disable_web_page_preview='yes')

        sleep(5)
