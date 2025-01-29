from enum import Enum


class HtmlPageElements(Enum):
    DIV = "div"
    IMG = "img"
    SPAN = "span"
    A = "a"
    ARTICLE = "article"
    H5 = "h5"


class HtmlAttrs(Enum):
    HREF = "href"


class HtmlClassNames(Enum):
    TITLE = "title"
    TODAY_1 = "today_1"
    AF_ACTIVE = "afishaItem active"
