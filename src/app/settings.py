from pydantic_settings import BaseSettings


class TelegramSettings(BaseSettings):

    bot_token: str
    chanel_name: str





