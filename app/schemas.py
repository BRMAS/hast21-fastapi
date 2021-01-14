#from datetime import date
from typing import Optional
from pydantic import BaseModel


class Person(BaseModel):
    pid: int
    lastName: Optional[str]
    firstName: Optional[str]
    nameC: Optional[str]
    nameOther: Optional[str]
    #collector:

    class Config:
        orm_mode = True
