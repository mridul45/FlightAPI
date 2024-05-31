from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Flight(BaseModel):

    airline: str
    flightNumber: int
    depCity: str
    arrCity: str
    price: int
    depDate: datetime
    arrDate: datetime
    duration: str
    returnDate: Optional[datetime] = None
    returnFlightNumber: Optional[str] = None
    returnDepCity: Optional[str] = None
    returnArrCity: Optional[str] = None
    returnDuration: Optional[str] = None
    returnStops: Optional[int] = None
