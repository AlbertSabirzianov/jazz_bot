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
                    name=div.find(HtmlPageElements.H3.value).text.replace('\n', ''),
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

