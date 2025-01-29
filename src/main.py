from app.interfaces import ConcertHallParser
from app.parsers import *

ALL_PARSERS: list[ConcertHallParser] = [
    KzlParser("https://kozlovclub.ru"),
    EsseParser("https://www.jazzesse.ru")
]


def main():
    for parser in ALL_PARSERS:
        print()
        for concert in parser.get_today_concerts():
            print(concert)


if __name__ == "__main__":
    main()
