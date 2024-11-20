from decimal import Decimal
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/contas-a-pagar-e-receber", tags=["Contas a Pagar e Receber"]
)


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str  # Pagar, Receber


class GetAllPagarReceberResponse(BaseModel):
    contas: List[ContaPagarReceberResponse]


class ContaPagarReceberRequest(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str


@router.get(
    "",
    responses={
        200: {
            "model": GetAllPagarReceberResponse,
        },
        400: {},
    },
)
def listar_contas():
    contas = {
        "contas": [
            ContaPagarReceberResponse(
                id=1, descricao="Aluguel", valor=690.50, tipo="PAGAR"
            ),
            ContaPagarReceberResponse(
                id=2, descricao="Salario", valor=7500, tipo="RECEBER"
            ),
        ]
    }

    return contas


@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest):
    return ContaPagarReceberResponse(
        id=3, descricao=conta.descricao, valor=conta.valor, tipo=conta.tipo
    )
