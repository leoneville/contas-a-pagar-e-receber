from enum import Enum
import json
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from sqlalchemy.orm import Session

from contas_a_pagar_e_receber.models.conta_a_pagar_receber_model import (
    ContaPagarReceber,
)
from shared.dependencies import get_db


router = APIRouter(
    prefix="/contas-a-pagar-e-receber", tags=["Contas a Pagar e Receber"]
)


class ContaPagarReceberTipoEnum(str, Enum):
    pagar = "PAGAR"
    receber = "RECEBER"


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: float
    tipo: ContaPagarReceberTipoEnum

    model_config = ConfigDict(from_attributes=True)


class GetAllPagarReceberResponse(BaseModel):
    contas: List[ContaPagarReceberResponse]


class ContaPagarReceberRequest(BaseModel):
    descricao: Annotated[str, StringConstraints(min_length=3, max_length=30)]
    valor: float = Field(gt=0)
    tipo: ContaPagarReceberTipoEnum


@router.get(
    "",
    responses={
        200: {
            "model": GetAllPagarReceberResponse,
        },
        400: {},
    },
)
def listar_contas(db: Session = Depends(get_db)) -> GetAllPagarReceberResponse:
    contas = db.query(ContaPagarReceber).all()

    response = GetAllPagarReceberResponse(
        contas=[ContaPagarReceberResponse.model_validate(conta) for conta in contas]
    )

    return response


@router.get(
    "/{id_da_conta_a_pagar_e_receber}",
    responses={200: {"model": ContaPagarReceberResponse}, 404: {}},
)
def lista_conta(
    id_da_conta_a_pagar_e_receber: int, db: Session = Depends(get_db)
) -> ContaPagarReceberResponse:
    conta_pagar_e_receber: ContaPagarReceber = db.query().session.get(
        ContaPagarReceber, id_da_conta_a_pagar_e_receber
    )
    if conta_pagar_e_receber is None:
        raise HTTPException(404, "Conta não encontrada.")

    return conta_pagar_e_receber


@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(
    conta_a_pagar_e_receber_request: ContaPagarReceberRequest,
    db: Session = Depends(get_db),
) -> ContaPagarReceberResponse:
    contas_a_pagar_e_receber = ContaPagarReceber(
        **conta_a_pagar_e_receber_request.model_dump()
    )

    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)

    return contas_a_pagar_e_receber


@router.put(
    "/{id_da_conta_a_pagar_e_receber}",
    response_model=ContaPagarReceberResponse,
    status_code=200,
)
def atualizar_conta(
    id_da_conta_a_pagar_e_receber: int,
    conta_a_pagar_e_receber_request: ContaPagarReceberRequest,
    db: Session = Depends(get_db),
) -> ContaPagarReceberResponse:
    conta_a_pagar_e_receber: ContaPagarReceber = db.query().session.get(
        ContaPagarReceber, id_da_conta_a_pagar_e_receber
    )
    conta_a_pagar_e_receber.tipo = conta_a_pagar_e_receber_request.tipo
    conta_a_pagar_e_receber.valor = conta_a_pagar_e_receber_request.valor
    conta_a_pagar_e_receber.descricao = conta_a_pagar_e_receber_request.descricao

    db.add(conta_a_pagar_e_receber)
    db.commit()
    db.refresh(conta_a_pagar_e_receber)
    return conta_a_pagar_e_receber


@router.delete("/{id_da_conta_a_pagar_e_receber}", status_code=204)
def deletar_conta(id_da_conta_a_pagar_e_receber: int, db: Session = Depends(get_db)):

    db.query(ContaPagarReceber).filter_by(id=id_da_conta_a_pagar_e_receber).delete()
    db.commit()

    return {}, 204
