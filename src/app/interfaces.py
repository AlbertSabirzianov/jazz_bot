from abc import ABC, abstractmethod

from .schema import Concert


class ConcertHallParser(ABC):

    def __init__(self, url: str):
        self.parse_url: str = url

    @abstractmethod
    def get_today_concerts(self) -> list[Concert]:
        raise NotImplementedError
