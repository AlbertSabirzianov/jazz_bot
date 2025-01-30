from .enums import HtmlPageElements, HtmlAttrs, HtmlClassNames
from .interfaces import ConcertHallParser
from .schema import Concert


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
                    hall_name=self.hall_name
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
                    hall_name=self.hall_name
                )
            )
        return concerts


class BtParser(ConcertHallParser):
    def get_today_concerts(self) -> list[Concert]:
        div = self.soup.find(HtmlPageElements.A.value, class_=HtmlClassNames.LINK_RESET.value)
        return [
            Concert(
                name=div.find(HtmlPageElements.IMG.value).get(HtmlAttrs.ALT.value),
                url=self.parse_url + div.get(HtmlAttrs.HREF.value),
                hall_name=self.hall_name
            )
        ]