import asyncio
import datetime
import time

from telegram import Bot
from dotenv import load_dotenv

from app.interfaces import ConcertHallParser
from app.parsers import *
from app.settings import TelegramSettings
from app.utils import get_message_from_concerts

ALL_PARSERS: list[ConcertHallParser] = [
    KzlParser("https://kozlovclub.ru", "Kozlov"),
    EsseParser("https://www.jazzesse.ru", "Esse"),
    BtParser("https://moscow.butmanclub.ru", "Butman")
]


def main():
    load_dotenv()
    telegram_settings = TelegramSettings()
    while True:
        concerts = []
        for parser in ALL_PARSERS:
            for concert in parser.get_today_concerts():
                print(concert)
                concerts.append(concert)
        message = get_message_from_concerts(concerts)
        bot = Bot(token=telegram_settings.bot_token)
        asyncio.run(
            bot.send_message(chat_id=telegram_settings.chanel_name, text=message, parse_mode='MarkdownV2')
        )
        time.sleep(datetime.timedelta(days=1).total_seconds())


if __name__ == "__main__":
    main()
