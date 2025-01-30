from enum import Enum


class HtmlPageElements(Enum):
    DIV = "div"
    IMG = "img"
    SPAN = "span"
    A = "a"
    ARTICLE = "article"
    H5 = "h5"
    H3 = "h3"


class HtmlAttrs(Enum):
    HREF = "href"
    ALT = "alt"


class HtmlClassNames(Enum):
    TITLE = "title"
    TODAY_1 = "today_1"
    AF_ACTIVE = "afishaItem active"
    LINK_RESET = "uk-link-reset"
    TICKETSCLOUD_EVENT = "ticketscloud-event-item col-md-4"
