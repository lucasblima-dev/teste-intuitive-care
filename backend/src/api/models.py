from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Operadora(Base):
    __tablename__ = "operadoras"

    reg_ans = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String)
    uf = Column(String)
    modalidade = Column(String)

    despesas = relationship("Despesa", back_populates="operadora")

class Despesa(Base):
    __tablename__ = "despesas"

    id = Column(Integer, primary_key=True, index=True)
    reg_ans = Column(Integer, ForeignKey("operadoras.reg_ans"))
    descricao_conta = Column(String)
    data_evento = Column(Date)
    trimestre = Column(String)
    ano = Column(Integer)
    valor = Column(Numeric(15, 2))

    operadora = relationship("Operadora", back_populates="despesas")