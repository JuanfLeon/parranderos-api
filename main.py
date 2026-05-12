from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#os.environ para despliegue. Descomente cuando ya probó todo local.
client = MongoClient(os.environ["MONGO_URI"])
# TODO: conectarse al cluster Admonsis  
#client = MongoClient("mongodb://ISIS2304D27202610:PGfMXdt1XNyg@157.253.236.88:8087")


# TODO: conectarse a la base de datos Admonsis  
db = client["ISIS2304D27202610"]
#db = client["ISIS2304"]


@app.get("/")
def root():
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(
        db["comentarios_bares"].find({"bar_id": bar_id})
    )
    for c in comentarios:
        c["_id"] = str(c["_id"])
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
    db["comentarios_bares"].insert_one(datos)
    datos["_id"] = str(datos["_id"])
    return {'mensaje': 'Comentario guardado'}

# TODO: implementar GET /bares/{bar_id}/eventos
# Debe retornar todos los eventos del bar desde la colección 'eventos'

# TODO: implementar POST /bares/{bar_id}/eventos  
# Debe insertar el evento en la colección 'eventos'
# Recuerde agregar bar_id y fecha_creacion al documento antes de insertar
