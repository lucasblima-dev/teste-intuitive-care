from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List

from . import models, schemas, database

router = APIRouter()

@router.get("/operadoras", response_model=schemas.PaginatedOperadoras)
def list_operadoras(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(database.get_db)
):
    offset = (page - 1) * limit
    query = db.query(models.Operadora)

    if search:
        query = query.filter(models.Operadora.razao_social.ilike(f"%{search}%"))

    total = query.count()
    operadoras = query.offset(offset).limit(limit).all()

    return {
        "data": operadoras,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/operadoras/{reg_ans}", response_model=schemas.OperadoraDetail)
def get_operadora(reg_ans: int, db: Session = Depends(database.get_db)):
    op = db.query(models.Operadora).filter(models.Operadora.reg_ans == reg_ans).first()
    if not op:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    return op

@router.get("/operadoras/{reg_ans}/despesas", response_model=List[schemas.DespesaBase])
def get_operadora_despesas(reg_ans: int, db: Session = Depends(database.get_db)):
    despesas = db.query(models.Despesa).filter(models.Despesa.reg_ans == reg_ans).all()
    return despesas

@router.get("/estatisticas", response_model=List[schemas.StatsUF])
def get_estatisticas(db: Session = Depends(database.get_db)):
    stats = db.query(
        models.Operadora.uf,
        func.sum(models.Despesa.valor).label("total_despesas")
    ).join(models.Despesa)\
     .filter(models.Operadora.uf.isnot(None))\
     .group_by(models.Operadora.uf)\
     .order_by(desc("total_despesas"))\
     .limit(5)\
     .all()
    
    return [{"uf": s.uf, "total_despesas": s.total_despesas} for s in stats]