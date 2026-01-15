from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from .schema import Concert
from .exceptions import AddressNotAllowed


class ConcertHallParser(ABC):
    """
    Абстрактный базовый класс для парсинга афиши концертов в различных концертных залах

    Класс предоставляет базовый функционал для работы с веб-страницами концертных залов,
    включая:
    * Получение HTML-содержимого страницы
    * Парсинг данных с помощью BeautifulSoup
    * Обработку ошибок подключения
    * Абстрактный метод для получения концертов текущего дня
    """

    def __init__(self, url: str, hall_name: str):
        """
        Инициализация парсера

        Аргументы:
        url (str): URL-адрес страницы концертного зала
        hall_name (str): Название концертного зала
        """
        self.parse_url: str = url
        self.hall_name: str = hall_name

    def set_query_params(self, params: dict[str, str]) -> None:
        """
        Установка параметров запроса путем замены значений в URL

        Аргументы:
        params (dict[str, str]): Словарь параметров для замены в URL
        """
        for key, value in params.items():
            self.parse_url = self.parse_url.replace(key, value)

    @property
    def response(self) -> requests.Response:
        """
        Получение HTTP-ответа с сервера с обработкой ошибок

        Метод выполняет до 3 попыток подключения к серверу.
        При неудаче поднимает исключение AddressNotAllowed
        """
        count = 3
        while count:
            try:
                return requests.get(self.parse_url)
            except requests.exceptions.RequestException:
                print(f"Can not connect to {self.parse_url}")
                count -= 1
        raise AddressNotAllowed(f"Address {self.hall_name} not allowed")

    @property
    def soup(self) -> BeautifulSoup:
        """
        Получение объекта BeautifulSoup с обработанным HTML-содержимым

        Метод:
        * Выполняет запрос к серверу
        * Устанавливает кодировку UTF-8
        * Парсит HTML с помощью BeautifulSoup
        * Обрабатывает ошибки подключения
        """
        count = 3
        while count:
            try:
                response = requests.get(self.parse_url)
                response.encoding = 'utf-8'
                return BeautifulSoup(response.text, features="lxml")
            except requests.exceptions.RequestException:
                print(f"Can not connect to {self.parse_url}")
                count -= 1
        raise AddressNotAllowed(f"Address {self.hall_name} not allowed")

    @abstractmethod
    def get_today_concerts(self) -> list[Concert]:
        """
        Абстрактный метод для получения концертов текущего дня

        Должен быть реализован в конкретных классах-наследниках
        и возвращать список объектов Concert
        """
        raise NotImplementedError
