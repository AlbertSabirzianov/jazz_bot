from enum import Enum


class HtmlPageElements(Enum):
    DIV = "div"
    IMG = "img"
    SPAN = "span"
    A = "a"
    ARTICLE = "article"
    H5 = "h5"
    H3 = "h3"
    P = "p"
    TIME = "time"


class HtmlAttrs(Enum):
    HREF = "href"
    ALT = "alt"
    TITLE = "title"


class HtmlClassNames(Enum):
    TITLE = "title"
    TODAY_1 = "today_1"
    AF_ACTIVE = "afishaItem active"
    LINK_RESET = "uk-link-reset"
    TICKETSCLOUD_EVENT = "ticketscloud-event-item col-md-4"
    ROW_ROW_1 = "row row_1"
    HOUR = "houre"
    COVER = "cover"
    ARTIST = "artist"

