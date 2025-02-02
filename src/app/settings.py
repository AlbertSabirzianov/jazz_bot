from pydantic_settings import BaseSettings


class PublicSettings(BaseSettings):

    time_to_publish: str = "09:00"


class TelegramSettings(BaseSettings):

    bot_token: str
    chanel_name: str





