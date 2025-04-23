from sqlalchemy import Column, String, DateTime, Enum
from database import Base
import enum

class EstadoVuelo(str, enum.Enum):
    programado = "programado"
    emergencia = "emergencia"
    retrasado = "retrasado"

class Vuelo(Base):
    __tablename__ = "vuelos"

    codigo = Column(String, primary_key=True, index=True)
    estado = Column(Enum(EstadoVuelo), nullable=False)
    hora_salida = Column(DateTime, nullable=False)
    origen = Column(String, nullable=False)
    destino = Column(String, nullable=False)
