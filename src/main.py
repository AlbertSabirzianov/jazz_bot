from dotenv import load_dotenv

from app.parsers import *
from app.services import send_concerts_to_chanel
from app.settings import TelegramSettings

ALL_MOSCOW_PARSERS: list[ConcertHallParser] = [
    KzlParser("https://kozlovclub.ru", "Джаз Клуб Алексея Козлова"),
    EsseParser("https://www.jazzesse.ru", "Джаз Клуб Эссе"),
    BtParser("https://moscow.butmanclub.ru", "Клуб Игоря Бутмана"),
    JamClubParser(
        "https://jamclub.ticketscloud.org/?tags=%D0%9A%D0%BE%D0%BD%D1%86%D0%B5%D1%80%D1%82%D1%8B&city=524901&starts_at=today&price=",
        "JamClub"
    ),
    UCClubParser("https://ucclub.ru", "Джаз клуб союз композиторов")
]


ALL_ST_PARSERS: list[ConcertHallParser] = [
    BtParser("https://spb.butmanclub.ru/", "Клуб Игоря Бутмана"),
    PhilharmonicJazzHall("https://jazz-hall.ru/afisha", "Филармония джазовой музыки"),
    JFCParser("https://jfc-club.spb.ru", "JFC Jazz Club"),
    PoliceStationParser(
        "https://wdt.bileter.ru/fd4773edb1ce0fd129b5cf61332a3c0c/ru/afisha/get-afisha?type=table",
        "ДЖАЗ-КЛУБ POLICE STATION"
    )
]


def main():
    telegram_settings = TelegramSettings()
    chanel_and_parsers: list[tuple[str, list[ConcertHallParser]]] = [
        (telegram_settings.moscow_chanel_name, ALL_MOSCOW_PARSERS),
        (telegram_settings.st_chanel_name, ALL_ST_PARSERS)
    ]
    for chanel_name, parsers in chanel_and_parsers:
        send_concerts_to_chanel(
            chanel_name=chanel_name,
            parsers=parsers,
            bot_token=telegram_settings.bot_token
        )


if __name__ == "__main__":
    load_dotenv()
    main()
