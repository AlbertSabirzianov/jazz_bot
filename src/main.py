import asyncio
import datetime
import pprint
import time

from telegram import Bot
from dotenv import load_dotenv

from app.interfaces import ConcertHallParser
from app.parsers import *
from app.settings import TelegramSettings
from app.utils import get_message_from_concerts, get_day_time_concerts_dict

ALL_PARSERS: list[ConcertHallParser] = [
    KzlParser("https://kozlovclub.ru", "Джаз Клуб Алексея Козлова"),
    EsseParser("https://www.jazzesse.ru", "Джаз Клуб Эссе"),
    BtParser("https://moscow.butmanclub.ru", "Клуб Игоря Бутмана"),
    JamClubParser(
        "https://jamclub.ticketscloud.org/?tags=%D0%9A%D0%BE%D0%BD%D1%86%D0%B5%D1%80%D1%82%D1%8B&city=524901&starts_at=today&price=",
        "JamClub"
    ),
    UCClubParser("https://ucclub.ru", "Джаз клуб союз композиторов")
]


def get_all_concerts(all_parsers: list[ConcertHallParser]) -> list[Concert]:
    concerts = []
    for parser in all_parsers:
        for concert in parser.get_today_concerts():
            print(concert)
            concerts.append(concert)
    return concerts


def get_messages_from_dict(day_time_concerts_dict: dict[str, list[Concert]]) -> list[str]:
    messages: list[str] = []
    for day_time in day_time_concerts_dict.keys():
        if day_time_concerts_dict[day_time]:
            messages.append(
                get_message_from_concerts(
                    day_time_concerts_dict[day_time],
                    day_time
                )
            )
    return messages


def main():
    load_dotenv()
    telegram_settings = TelegramSettings()
    while True:
        concerts: list[Concert] = get_all_concerts(ALL_PARSERS)
        day_time_concerts_dict: dict[str, list[Concert]] = get_day_time_concerts_dict(concerts)
        messages: list[str] = get_messages_from_dict(day_time_concerts_dict)
        for message in messages:
            bot = Bot(token=telegram_settings.bot_token)
            asyncio.run(
                bot.send_message(chat_id=telegram_settings.chanel_name, text=message, parse_mode='MarkdownV2')
            )
        time.sleep(datetime.timedelta(days=1).total_seconds())


if __name__ == "__main__":
    main()
