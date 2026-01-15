"""
Модуль парсеров для конкретных джаз-клубов

Каждый парсер реализует специфичную логику извлечения информации о концертах
с учетом структуры HTML-страниц соответствующих сайтов.

Основные особенности модуля:
* Использование единого интерфейса ConcertHallParser
* Работа с HTML-структурой через BeautifulSoup
* Формирование объектов Concert с корректной обработкой данных
* Обработка специфичных CSS-классов и HTML-элементов каждой площадки

Для работы модуля используются следующие компоненты:
* bs4 и BeautifulSoup для парсинга HTML
* requests для выполнения HTTP-запросов
* Enum-классы для хранения HTML-элементов и атрибутов
* Интерфейс ConcertHallParser как базовый класс
* Схема Concert для структурирования данных о концертах
"""
import datetime

import bs4
import requests
from bs4 import BeautifulSoup

from .enums import HtmlPageElements, HtmlAttrs, HtmlClassNames
from .interfaces import ConcertHallParser
from .schema import Concert
from .utils import concat_urls


class KzlParser(ConcertHallParser):

    def get_today_concerts(self) -> list[Concert]:
        concerts: list = []
        divs = self.soup.find_all(HtmlPageElements.DIV.value, class_=HtmlClassNames.TODAY_1.value)
        for d in divs:
            concerts.append(
                Concert(
                    name=d.find(HtmlPageElements.A.value, class_=HtmlClassNames.TITLE.value).text,
                    url=self.parse_url + d.find(
                        HtmlPageElements.A.value,
                        class_=HtmlClassNames.TITLE.value
                    ).get(
                        HtmlAttrs.HREF.value
                    ),
                    hall_name=self.hall_name,
                    time=str(
                        d.find(
                            HtmlPageElements.DIV.value,
                            class_=HtmlClassNames.ROW_ROW_1.value
                        ).text
                    ).split(" | ")[1]
                )
            )
        return concerts


class EsseParser(ConcertHallParser):

    def get_today_concerts(self) -> list[Concert]:
        divs = self.soup.find_all(HtmlPageElements.ARTICLE.value, class_=HtmlClassNames.AF_ACTIVE.value)
        concerts = []
        for d in divs:
            concerts.append(
                Concert(
                    name=d.find(
                        HtmlPageElements.H5.value
                    ).find(
                        HtmlPageElements.A.value
                    ).text.replace('\t', '').replace('\n', ''),
                    url=self.parse_url + d.find(
                        HtmlPageElements.H5.value
                    ).find(
                        HtmlPageElements.A.value
                    ).get(
                        HtmlAttrs.HREF.value
                    ).replace('\t', '').replace('\n', ''),
                    hall_name=self.hall_name,
                    time=d.find(HtmlPageElements.DIV.value, class_=HtmlClassNames.HOUR.value).text
                )
            )
        return concerts


class BtParser(ConcertHallParser):
    def get_today_concerts(self) -> list[Concert]:
        divs = self.soup.find_all(HtmlPageElements.A.value, class_=HtmlClassNames.LINK_RESET.value)
        return [
            Concert(
                name=divs[0].find(HtmlPageElements.IMG.value).get(HtmlAttrs.ALT.value),
                url=self.parse_url + divs[0].get(HtmlAttrs.HREF.value),
                hall_name=self.hall_name,
                time=divs[1].find(HtmlPageElements.P.value).text.split(" / ")[1]
            )
        ]


class JamClubParser(ConcertHallParser):
    def get_today_concerts(self) -> list[Concert]:
        divs = self.soup.find_all(
            HtmlPageElements.DIV.value,
            class_=HtmlClassNames.TICKETSCLOUD_EVENT.value
        )[1:]
        concerts = []
        for div in divs:
            concerts.append(
                Concert(
                    name=div.find(HtmlPageElements.P.value).text.replace('\n', ''),
                    hall_name=self.hall_name,
                    url=concat_urls(self.parse_url, div.find(HtmlPageElements.A.value).get(HtmlAttrs.HREF.value)),
                    time=div.find(HtmlPageElements.TIME.value).text.split()[1]
                )
            )
        return concerts


class UCClubParser(ConcertHallParser):
    def get_today_concerts(self) -> list[Concert]:
        divs = self.soup.find_all(HtmlPageElements.DIV.value, class_=HtmlClassNames.COVER.value)
        today_divs = list(
            filter(
                lambda x: "СЕГОДНЯ" in x.find(
                    HtmlPageElements.DIV.value,
                    class_=HtmlClassNames.TITLE.value
                ).text,
                divs
            )
        )
        concerts = []
        for div in today_divs:
            concerts.append(
                Concert(
                    name=div.find(
                        HtmlPageElements.DIV.value,
                        class_=HtmlClassNames.ARTIST.value
                    ).text.split('\n')[0],
                    hall_name=self.hall_name,
                    url=self.parse_url + div.find(HtmlPageElements.A.value).get(HtmlAttrs.HREF.value),
                    time=div.find(
                        HtmlPageElements.DIV.value,
                        class_=HtmlClassNames.TITLE.value
                    ).text.split()[1]
                )
            )
        return concerts


class PhilharmonicJazzHall(ConcertHallParser):
    def get_today_concerts(self) -> list[Concert]:
        divs = self.soup.find_all(
            HtmlPageElements.DIV.value,
            class_="afisha__list-item afisha__list-item-sale"
        )[:3]
        divs = list(
            filter(
                lambda div: str(datetime.datetime.now().day) in div.find(
                    HtmlPageElements.DIV.value,
                    class_="afisha__list-item-date"
                ).text,
                divs
            )
        )
        return [
            Concert(
                hall_name=self.hall_name,
                url=self.parse_url + str(
                    div.find(
                        HtmlPageElements.A.value
                    ).get(
                        HtmlAttrs.HREF.value
                    )
                ).replace("/afisha", ""),
                name=div.find(
                    HtmlPageElements.DIV.value,
                    class_="afisha__list-item-content"
                ).find(
                    HtmlPageElements.DIV.value
                ).find(
                    HtmlPageElements.A.value
                ).text.replace("\t", "").replace("\n", ""),
                time=div.find(
                    HtmlPageElements.DIV.value,
                    class_="afisha__list-item-content"
                ).find(
                    HtmlPageElements.DIV.value
                ).find(
                    HtmlPageElements.P.value
                ).text.replace("\t", "").replace("\n", "")
            ) for div in divs
        ]


class JFCParser(ConcertHallParser):

    @staticmethod
    def __is_today_concert(div: bs4.BeautifulSoup) -> bool:
        day = div.find(
            HtmlPageElements.DIV.value,
            class_="bprev_date"
        ).text[:5]
        return int(
            day.split(".")[0]
        ) == datetime.datetime.now().day and int(
            day.split(".")[1]
        ) == datetime.datetime.now().month

    def get_today_concerts(self) -> list[Concert]:
        divs = self.soup.find_all(
            HtmlPageElements.DIV.value,
            class_="bprev"
        )
        divs = list(
            filter(
                self.__is_today_concert,
                divs
            )
        )
        return [
            Concert(
                hall_name=self.hall_name,
                url=self.parse_url + div.find(
                    HtmlPageElements.DIV.value,
                    class_="bprev_link"
                ).find(
                    HtmlPageElements.A.value
                ).get(HtmlAttrs.HREF.value),
                time=div.find(HtmlPageElements.SPAN.value, class_="concert_time").text,
                name=div.find(
                    HtmlPageElements.DIV.value,
                    class_="bprev_link"
                ).find(
                    HtmlPageElements.A.value
                ).get(HtmlAttrs.TITLE.value).split("/")[1]
            ) for div in divs
        ]


class PoliceStationParser(ConcertHallParser):

    @property
    def soup(self) -> BeautifulSoup:
        while True:
            try:
                response = requests.get(self.parse_url)
                return BeautifulSoup(response.json()['html'], features="lxml")
            except requests.exceptions.RequestException:
                print(f"Can not connect to {self.parse_url}")

    def get_today_concerts(self) -> list[Concert]:
        divs = self.soup.find_all(
            HtmlPageElements.DIV.value,
            class_="wb-afisha__event"
        )
        divs = filter(
            lambda x: "Сегодня" in x.find(HtmlPageElements.DIV.value, class_="wb-afisha__weekday").text,
            divs
        )
        return [
            Concert(
                hall_name=self.hall_name,
                url="https://police-station.ru",
                name=str(
                    div.find(
                        HtmlPageElements.DIV.value,
                        class_="wb-afisha__event-name"
                    ).text.replace("\n", "")).strip(),
                time=str(
                    div.find(
                        HtmlPageElements.DIV.value,
                        class_="wb-afisha__start-time"
                    ).text
                ).split()[-1]
            ) for div in divs
        ]


class TatPhilharmonicParser(ConcertHallParser):
    def get_today_concerts(self) -> list[Concert]:
        divs = self.soup.find_all(HtmlPageElements.DIV.value, class_="poster-item")
        divs = filter(
            lambda x: int(
                x.find(
                    HtmlPageElements.SPAN.value,
                    class_="poster-item__date-number"
                ).text
            ) == datetime.datetime.now().day and x.find(HtmlPageElements.SPAN.value, class_="label").text == "Джаз",
            divs
        )
        return [
            Concert(
                hall_name=self.hall_name,
                url=self.parse_url + div.find(HtmlPageElements.A.value).get(HtmlAttrs.HREF.value),
                name=div.find(HtmlPageElements.H4.value).text,
                time=div.find(HtmlPageElements.SPAN.value, class_="poster-item__time").text
            ) for div in divs
        ]


class OldPianoParser(ConcertHallParser):
    def get_today_concerts(self) -> list[Concert]:
        self.set_query_params(
            {
                "<timeMin_value>": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                "<timeMax_value>": datetime.datetime.now().strftime('%Y-%m-%d')
            }
        )
        return [
            Concert(
                hall_name=self.hall_name,
                url="http://starroyal.ru",
                name=str(item["summary"]).split("/")[0],
                time=str(item["start"]["dateTime"]).split("T")[1][:5]
            ) for item in self.response.json()["items"]
        ]


class RostovEsseParser(ConcertHallParser):
    def get_today_concerts(self) -> list[Concert]:
        items = filter(
            lambda item: item["date"].split("T")[0] == datetime.datetime.now().strftime('%Y-%m-%d'),
            self.response.json()["data"]
        )
        return [
            Concert(
                hall_name=self.hall_name,
                url=item["booking_url"],
                name=item["title"],
                time=item["date"].split("T")[1]
            ) for item in items
        ]
