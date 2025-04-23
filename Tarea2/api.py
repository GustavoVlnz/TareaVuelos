from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from database import get_db
from models import Vuelo
from schemas import VueloCreate
from schemas import VueloBase
from listaVueloss import ListaVuelos

router = APIRouter()

@router.on_event("startup")
def init_lista():
    global lista_vuelos
    db = next(get_db())
    lista_vuelos = ListaVuelos(db)

@router.post("/vuelos/frente")
def insertar_frente(vuelo: VueloCreate):
    nuevo = Vuelo(**vuelo.dict())
    lista_vuelos.insertar_al_frente(nuevo)
    return {"mensaje": "Vuelo insertado al frente", "vuelo": nuevo}

@router.post("/vuelos/final")
def insertar_final(vuelo: VueloCreate):
    nuevo = Vuelo(**vuelo.dict())
    lista_vuelos.insertar_al_final(nuevo)
    return {"mensaje": "Vuelo insertado al final", "vuelo": nuevo}

@router.get("/vuelos/primero", response_model=VueloBase)
def obtener_primero():
    vuelo = lista_vuelos.obtener_primero()
    if vuelo is None:
        raise HTTPException(status_code=404, detail="No hay vuelos")
    return vuelo

@router.get("/vuelos/ultimo", response_model=VueloBase)
def obtener_ultimo():
    vuelo = lista_vuelos.obtener_ultimo()
    if vuelo is None:
        raise HTTPException(status_code=404, detail="No hay vuelos")
    return vuelo

@router.get("/vuelos/longitud")
def obtener_longitud():
    return {"total_vuelos": lista_vuelos.longitud()}

@router.post("/vuelos/posicion/{posicion}")
def insertar_en_posicion(posicion: int, vuelo: VueloCreate = Body(...)):
    nuevo = Vuelo(**vuelo.dict())
    lista_vuelos.insertar_en_posicion(nuevo, posicion)
    return {"mensaje": f"Vuelo insertado en posicion {posicion}", "vuelo": nuevo}

@router.delete("/vuelos/posicion/{posicion}")
def eliminar_en_posicion(posicion: int):
    vuelo = lista_vuelos.extraer_de_posicion(posicion)
    if vuelo is None:
        raise HTTPException(status_code=404, detail="Posicion invalida")
    return {"mensaje": "Vuelo eliminado", "vuelo": vuelo}
