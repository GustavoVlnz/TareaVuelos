from pydantic import BaseModel
from datetime import datetime
from models import EstadoVuelo

class VueloBase(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora_salida: datetime
    origen: str
    destino: str

class VueloCreate(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora_salida: datetime
    origen: str
    destino: str


class VueloSchema(BaseModel):
    class Config:
        from_attributes = True
