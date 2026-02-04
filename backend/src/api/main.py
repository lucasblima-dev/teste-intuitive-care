from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, routes

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Intuitive Care API",
    version="1.0.0",
    description="API para consulta de dados da ANS e despesas de operadoras."
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/api", tags=["Operadoras"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API ok!"}
