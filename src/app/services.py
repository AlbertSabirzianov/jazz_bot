"""
Модуль для работы с Telegram API и отправки уведомлений о концертах

Данный модуль содержит функционал для:
* Отправки сообщений в Telegram-каналы
* Обработки ошибок при отправке
* Агрегации данных о концертах
* Форматирования и отправки уведомлений

Основные компоненты:
* Декоратор для повторных попыток отправки
* Функции для работы с концертами
* Методы отправки сообщений в каналы
"""
import asyncio
from typing import Optional

import telegram.error
from telegram import Bot

from .interfaces import ConcertHallParser
from .schema import Concert
from .utils import get_message_from_concerts, get_day_time_concerts_dict
from .settings import TelegramSettings


def retry_until_success(func):
    """
    Декоратор для повторных попыток отправки сообщений

    Параметры:
    func: Функция, которую нужно обернуть

    Возвращает:
    wrapper: Обернутая функция с обработкой ошибок
    """
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
    """
    Отправка сообщения в Telegram-канал

    Параметры:
    chanel_name (str): Имя канала
    bot_token (str): Токен бота
    message (str): Текст сообщения
    parse_mode (Optional[str]): Режим парсинга (по умолчанию MarkdownV2)
    """
    bot = Bot(token=bot_token)
    asyncio.run(
        bot.send_message(chat_id=chanel_name, text=message, parse_mode=parse_mode)
    )


def get_all_concerts(all_parsers: list[ConcertHallParser]) -> list[Concert]:
    """
    Получение всех концертов от всех парсеров

    Параметры:
    all_parsers (list[ConcertHallParser]): Список парсеров

    Возвращает:
    list[Concert]: Список всех концертов
    """
    concerts = []
    for parser in all_parsers:
        try:
            for concert in parser.get_today_concerts():
                print(concert)
                concerts.append(concert)
        except Exception:
            pass
    return concerts


def get_messages_from_dict(day_time_concerts_dict: dict[str, list[Concert]]) -> list[str]:
    """
    Формирование сообщений из словаря концертов

    Параметры:
    day_time_concerts_dict (dict[str, list[Concert]]): Словарь концертов по времени

    Возвращает:
    list[str]: Список готовых сообщений
    """
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
    """
    Основная функция отправки концертов в канал

    Параметры:
    chanel_name (str): Имя канала
    parsers (list[ConcertHallParser]): Список парсеров
    bot_token (str): Токен бота
    """
    concerts: list[Concert] = get_all_concerts(parsers)
    day_time_concerts_dict: dict[str, list[Concert]] = get_day_time_concerts_dict(concerts)
    messages: list[str] = get_messages_from_dict(day_time_concerts_dict)
    for message in messages:
        send_message_to_chanel(
            chanel_name=chanel_name,
            bot_token=bot_token,
            message=message
        )
