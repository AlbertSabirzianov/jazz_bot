import time
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

from .schema import Concert
from .exceptions import AddressNotAllowed


class SDriver:
    """
    Контекстный менеджер для инициализации и корректного завершения
    Selenium WebDriver с настройками для скрытия автоматизации.

    Использует ChromeDriver с опциями:
        - headless режим
        - отключение sandbox и shared memory
        - применение stealth-методов для маскировки автоматизации
        - установка пользовательского User-Agent

    Пример использования:
        with SDriver() as driver:
            driver.get("https://example.com")
    """
    def __enter__(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Windows",
            webgl_vendor="Google Inc.",
            render="WebKit",
            fix_hairline=True
        )
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


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


    def selenium_soup(self, waiting_element: str = "div.events") -> BeautifulSoup:
        count = 3
        while count:
            try:
                with SDriver() as driver:
                    driver.get(self.parse_url)
                    _ = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, waiting_element))
                    )

                    return BeautifulSoup(driver.page_source, features="lxml")
            except Exception:
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
