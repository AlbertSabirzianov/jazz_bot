from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from .schema import Concert


class ConcertHallParser(ABC):

    def __init__(self, url: str, hall_name: str):
        self.parse_url: str = url
        self.hall_name: str = hall_name

    def set_query_params(self, params: dict[str, str]) -> None:
        for key, value in params.items():
            self.parse_url = self.parse_url.replace(key, value)

    @property
    def response(self) -> requests.Response:
        while True:
            try:
                return requests.get(self.parse_url)
            except requests.exceptions.RequestException:
                print(f"Can not connect to {self.parse_url}")

    @property
    def soup(self) -> BeautifulSoup:
        while True:
            try:
                response = requests.get(self.parse_url)
                response.encoding = 'utf-8'
                return BeautifulSoup(response.text, features="lxml")
            except requests.exceptions.RequestException:
                print(f"Can not connect to {self.parse_url}")

    @abstractmethod
    def get_today_concerts(self) -> list[Concert]:
        raise NotImplementedError
