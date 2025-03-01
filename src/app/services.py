import asyncio
from typing import Optional

import telegram.error
from telegram import Bot

from .interfaces import ConcertHallParser
from .schema import Concert
from .utils import get_message_from_concerts, get_day_time_concerts_dict
from .settings import TelegramSettings


def retry_until_success(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except telegram.error.TelegramError:
                print(f"Cant send to telegram ...")
                continue
    return wrapper


@retry_until_success
def send_message_to_chanel(chanel_name: str, bot_token: str, message: str, parse_mode: Optional[str] = 'MarkdownV2') -> None:
    bot = Bot(token=bot_token)
    asyncio.run(
        bot.send_message(chat_id=chanel_name, text=message, parse_mode=parse_mode)
    )


def get_all_concerts(all_parsers: list[ConcertHallParser]) -> list[Concert]:
    telegram_settings = TelegramSettings()
    concerts = []
    for parser in all_parsers:
        try:
            for concert in parser.get_today_concerts():
                print(concert)
                concerts.append(concert)
        except Exception as err:
            send_message_to_chanel(
                chanel_name=telegram_settings.test_chanel_name,
                bot_token=telegram_settings.bot_token,
                message=f"Error in {parser.hall_name}" + "\n" + str(err),
                parse_mode=None
            )
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


def send_concerts_to_chanel(chanel_name: str, parsers: list[ConcertHallParser], bot_token: str) -> None:
    concerts: list[Concert] = get_all_concerts(parsers)
    day_time_concerts_dict: dict[str, list[Concert]] = get_day_time_concerts_dict(concerts)
    messages: list[str] = get_messages_from_dict(day_time_concerts_dict)
    for message in messages:
        send_message_to_chanel(
            chanel_name=chanel_name,
            bot_token=bot_token,
            message=message
        )
