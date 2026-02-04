from fastapi import FastAPI
from . import models, database, routes

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Intuitive Care API",
    version="1.0.0",
    description="API para consulta de dados da ANS e despesas de operadoras."
)

app.include_router(routes.router, prefix="/api", tags=["Operadoras"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API ok!"}