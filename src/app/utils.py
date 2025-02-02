from urllib.parse import urlparse, urlunparse, urljoin

from .schema import Concert


def escape_markdown(text):
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
    message = escape_markdown(f"🌟 Сегодня {day_time}!\n\n")
    for concert in concerts:
        message += f"📍 *{escape_markdown(concert.name.strip())}*\n[{concert.hall_name}]({concert.url}) {concert.time}\n\n"
    return message


def get_day_time_concerts_dict(concerts: list[Concert]) -> dict[str, list[Concert]]:
    return {
        "утром": list(filter(lambda x: x.hour < 12, concerts)),
        "днём": list(filter(lambda x: 12 <= x.hour <= 17, concerts)),
        "вечером": list(filter(lambda x: 17 < x.hour < 23, concerts)),
        "ночью": list(filter(lambda x: x.hour >= 23, concerts))
    }


def concat_urls(base_url: str, relative_url: str) -> str:
    # Парсим базовый URL
    parsed_base = urlparse(base_url)
    # Создаем новый URL без параметров
    new_base = urlunparse(parsed_base._replace(query=''))
    # Соединяем новый базовый URL с относительным URL
    return urljoin(new_base, relative_url)
