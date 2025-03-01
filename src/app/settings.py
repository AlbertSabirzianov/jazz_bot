from pydantic_settings import BaseSettings


class TelegramSettings(BaseSettings):

    bot_token: str
    moscow_chanel_name: str
    st_chanel_name: str
    kz_chanel_name: str
    rostov_chanel_name: str
    test_chanel_name: str





