from pydantic import BaseModel


class Concert(BaseModel):
    name: str
    url: str
    hall_name: str
    time: str

    @property
    def hour(self) -> int:
        if not self.time:
            self.time = "19:00"
        return int(self.time.split(":")[0])
