from enum import Enum


class HtmlPageElements(Enum):
    """
    Перечисление основных HTML-тегов, используемых при парсинге веб-страниц

    Атрибуты:
    DIV - базовый контейнерный элемент
    IMG - изображение
    SPAN - строчный контейнер
    A - гиперссылка
    ARTICLE - самостоятельный смысловой блок
    H5, H3, H4 - заголовки разных уровней
    P - абзац текста
    TIME - элемент для отображения времени или даты
    """
    DIV = "div"
    IMG = "img"
    SPAN = "span"
    A = "a"
    ARTICLE = "article"
    H5 = "h5"
    H3 = "h3"
    H4 = "h4"
    P = "p"
    TIME = "time"


class HtmlAttrs(Enum):
    """
    Перечисление основных HTML-атрибутов, используемых при парсинге

    Атрибуты:
    HREF - ссылка для тега <a>
    ALT - альтернативный текст для изображений
    TITLE - всплывающая подсказка
    """
    HREF = "href"
    ALT = "alt"
    TITLE = "title"


class HtmlClassNames(Enum):
    """
    Перечисление специфичных CSS-классов, используемых на целевых веб-страницах

    Атрибуты:
    TITLE - класс для заголовков
    TODAY_1 - класс для отображения событий текущего дня
    AF_ACTIVE - активный элемент афиши
    LINK_RESET - сброс стилей для ссылок
    TICKETSCLOUD_EVENT - элемент события в системе TicketCloud
    ROW_ROW_1 - структура строки с модификатором
    HOUR - отображение времени
    COVER - обложка события
    ARTIST - информация об исполнителе
    """
    TITLE = "title"
    TODAY_1 = "today_1"
    AF_ACTIVE = "afishaItem active"
    LINK_RESET = "uk-link-reset"
    TICKETSCLOUD_EVENT = "ticketscloud-event-item col-md-4"
    ROW_ROW_1 = "row row_1"
    HOUR = "houre"
    COVER = "cover"
    ARTIST = "artist"

