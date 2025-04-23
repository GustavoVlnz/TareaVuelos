from fastapi import FastAPI
from api import router
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestion de Vuelos")
app.include_router(router)
