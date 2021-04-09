from datetime import datetime, date, time
from pydantic import BaseModel
from typing import Optional


class WeatherDailyRecordSchemaModel(BaseModel):
    newRecordDate: date
    avgT: float
    minT: float
    maxT: float
    precip: float


class WeatherHourlyRecordSchemaModel(BaseModel):

   
    time: datetime
    recDate: date
    recHour: time
    temp: Optional[float]
    dwpt: Optional[float]
    rhum: Optional[float]
    prcp: Optional[float]
    snow: Optional[float]
    wdir: Optional[int]
    wspd: Optional[float]
    wpgt: Optional[float]
    pres: Optional[float]
    tsun: Optional[float]
    coco: Optional[int]
    



