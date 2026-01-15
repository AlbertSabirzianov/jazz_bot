"""
Модуль утилит для работы с данными концертов и Telegram-форматированием

Содержит вспомогательные функции для:
* Экранирования Markdown-символов
* Форматирования сообщений о концертах
* Группировки концертов по времени суток
* Работы с URL-адресами
"""
from urllib.parse import urlparse, urlunparse, urljoin

from .schema import Concert


def escape_markdown(text):
    """
    Экранирование специальных символов Markdown

    Параметры:
    text (str): Исходный текст для экранирования

    Возвращает:
    str: Текст с экранированными специальными символами
    """
    # Словарь специальных символов и их экранированных версий
    escape_chars = {
        '\\': '\\\\',
        '*': '\\*',
        '_': '\\_',
        '[': '\\[',
        ']': '\\]',
        '(': '\\(',
        ')': '\\)',
        '~': '\\~',
        '`': '\\`',
        '>': '\\>',
        '#': '\\#',
        '+': '\\+',
        '-': '\\-',
        '=': '\\=',
        '|': '\\|',
        '{': '\\{',
        '}': '\\}',
        '.': '\\.',
        '!': '\\!'
    }

    # Экранируем каждый специальный символ в тексте
    for char, escaped in escape_chars.items():
        text = text.replace(char, escaped)

    return text


def get_message_from_concerts(concerts: list[Concert], day_time: str) -> str:
    """
    Формирование сообщения о концертах для Telegram

    Параметры:
    concerts (List[Concert]): Список концертов
    day_time (str): Время суток

    Возвращает:
    str: Сформированное сообщение в формате Markdown
    """
    message = escape_markdown(f"🌟 Сегодня {day_time}!\n\n")
    for concert in concerts:
        message += f"📍 *{escape_markdown(concert.name.strip())}*\n[{concert.hall_name}]({concert.url}) {concert.time}\n\n"
    return message


def get_day_time_concerts_dict(concerts: list[Concert]) -> dict[str, list[Concert]]:
    """
    Группировка концертов по времени суток

    Параметры:
    concerts (List[Concert]): Список всех концертов

    Возвращает:
    dict[str, List[Concert]]: Словарь с группами концертов по времени
    """
    return {
        "утром": list(filter(lambda x: x.hour < 12, concerts)),
        "днём": list(filter(lambda x: 12 <= x.hour <= 17, concerts)),
        "вечером": list(filter(lambda x: 17 < x.hour < 23, concerts)),
        "ночью": list(filter(lambda x: x.hour >= 23, concerts))
    }


def concat_urls(base_url: str, relative_url: str) -> str:
    """
    Соединение базового и относительного URL

    Параметры:
    base_url (str): Базовый URL
    relative_url (str): Относительный URL

    Возвращает:
    str: Полный URL
    """
    parsed_base = urlparse(base_url)
    new_base = urlunparse(parsed_base._replace(query=''))
    return urljoin(new_base, relative_url)
