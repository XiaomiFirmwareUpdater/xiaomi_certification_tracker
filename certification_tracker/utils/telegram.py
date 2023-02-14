"""Telegram Bot implementation"""
import json
from pathlib import Path
from time import sleep

from requests import post


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
        """
        self.config: dict = json.loads((Path(__file__).parent.parent.parent / "telegram_config.json").read_text())
        self.bot_token: str = self.config.get('tg_bot_token')
        chats = self.config.get('tg_chats')
        self.chats = [int(chat) if chat.startswith('-') else f"@{chat}" for chat in chats]

    def send_telegram_message(self, message: str):
        """
        Send a message to Telegram chat
        :param message: A string of the update message to be sent
        :return:
        """
        for chat in self.chats:
            message = f"{message}\n{self.chats[0]}"
            params = {
                'chat_id': chat,
                'text': message,
                'parse_mode': "Markdown",
                'disable_web_page_preview': "yes"
            }
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            post(url, data=params)
            sleep(5)
