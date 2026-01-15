from pydantic_settings import BaseSettings


class TelegramSettings(BaseSettings):
    """
    Класс настроек для работы с Telegram API

    Содержит параметры для подключения к различным Telegram-каналам
    и настройки бота.

    Обязательные параметры:
    * bot_token: Токен Telegram-бота
    * moscow_chanel_name: Имя канала для Москвы
    * st_chanel_name: Имя канала для Санкт-Петербурга
    * kz_chanel_name: Имя канала для Казани
    * rostov_chanel_name: Имя канала для Ростова
    * test_chanel_name: Имя тестового канала
    """
    bot_token: str
    moscow_chanel_name: str
    st_chanel_name: str
    kz_chanel_name: str
    rostov_chanel_name: str
    test_chanel_name: str





