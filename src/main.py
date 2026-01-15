from dotenv import load_dotenv

from app.parsers import *
from app.services import send_concerts_to_chanel
from app.settings import TelegramSettings

ALL_MOSCOW_PARSERS: list[ConcertHallParser] = [
    BtParser("https://moscow.butmanclub.ru", "Клуб Игоря Бутмана"),
    KzlParser("https://kozlovclub.ru", "Джаз Клуб Алексея Козлова"),
    EsseParser("https://www.jazzesse.ru", "Джаз Клуб Эссе"),
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
        "ДЖАЗ КЛУБ POLICE STATION"
    )
]

ALL_KZ_PARSERS: list[ConcertHallParser] = [
    OldPianoParser(
        "https://clients6.google.com/calendar/v3/calendars/starroyal.adm%40gmail.com/events?"
        "calendarId=starroyal.adm%40gmail.com&singleEvents=true&eventTypes=default&eventTypes=focus"
        "Time&eventTypes=outOfOffice&timeZone=Europe%2FMoscow&maxAttendees=1&maxResults=250&sanitizeHtml=true&timeMin"
        "=<timeMin_value>T00%3A00%3A00%2B18%3A00&timeMax=<timeMax_value>T00%3A00%3A00-18%3A00&key=AIzaSyDOtGM5jr8bNp1ut"
        "VpG2_gSRH03RNGBkI8&%24unique=gc237",
        "Старый Рояль"
    ),
    TatPhilharmonicParser(
        "https://tatfil.ru",
        "Татарская государственная филармония имени Габдулы Тукая"
    )
]

ALL_ROSTOV_PARSERS: list[ConcertHallParser] = [
    RostovEsseParser(
        "https://essedon.ru/api/events?/limit=9&offset=0&is_active=true",
        "Джаз Клуб Эссе"
    )
]


def main():
    telegram_settings = TelegramSettings()
    chanel_and_parsers: list[tuple[str, list[ConcertHallParser]]] = [
        (telegram_settings.moscow_chanel_name, ALL_MOSCOW_PARSERS),
        (telegram_settings.st_chanel_name, ALL_ST_PARSERS),
        (telegram_settings.kz_chanel_name, ALL_KZ_PARSERS),
        (telegram_settings.rostov_chanel_name, ALL_ROSTOV_PARSERS)
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
