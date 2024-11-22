from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import Column, Integer, Numeric, String
from shared.database import Base


@dataclass
class ContaPagarReceber(Base):
    __tablename__ = "contas_a_pagar_e_receber"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    descricao: str = Column(String(30))
    valor: float = Column(Numeric(15, 2))
    tipo: str = Column(String(30))
