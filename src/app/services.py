import asyncio

from telegram import Bot

from .interfaces import ConcertHallParser
from .schema import Concert
from .utils import get_message_from_concerts, get_day_time_concerts_dict


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


def send_concerts_to_chanel(chanel_name: str, parsers: list[ConcertHallParser], bot_token: str) -> None:
    concerts: list[Concert] = get_all_concerts(parsers)
    day_time_concerts_dict: dict[str, list[Concert]] = get_day_time_concerts_dict(concerts)
    messages: list[str] = get_messages_from_dict(day_time_concerts_dict)
    for message in messages:
        bot = Bot(token=bot_token)
        asyncio.run(
            bot.send_message(chat_id=chanel_name, text=message, parse_mode='MarkdownV2')
        )
