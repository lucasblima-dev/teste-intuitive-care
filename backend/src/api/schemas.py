from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class OperadoraBase(BaseModel):
    reg_ans: int
    razao_social: Optional[str] = None
    uf: Optional[str] = None

    class Config:
        from_attributes = True

class DespesaBase(BaseModel):
    descricao_conta: str
    ano: int
    trimestre: str
    valor: float

    class Config:
        from_attributes = True

class OperadoraDetail(OperadoraBase):
    pass

class OperadoraComDespesas(OperadoraBase):
    despesas: List[DespesaBase] = []

class PaginatedOperadoras(BaseModel):
    data: List[OperadoraBase]
    total: int
    page: int
    limit: int

class StatsUF(BaseModel):
    uf: str
    total_despesas: float
    # media_por_lancamento: float