from pydantic import BaseModel


class Concert(BaseModel):
    name: str
    url: str
    hall_name: str
    time: str
