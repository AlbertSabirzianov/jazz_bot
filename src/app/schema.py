from pydantic import BaseModel


class Concert(BaseModel):
    name: str
    url: str
    hall_name: str
    time: str

    @property
    def hour(self) -> int:
        return int(self.time.split(":")[0])
