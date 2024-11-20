from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_deve_listar_contas_a_pagar_e_receber():
    response = client.get("/contas-a-pagar-e-receber")

    assert response.status_code == 200
    assert response.json()["contas"] == [
        {
            "descricao": "Aluguel",
            "id": 1,
            "tipo": "PAGAR",
            "valor": "690.5",
        },
        {
            "descricao": "Salario",
            "id": 2,
            "tipo": "RECEBER",
            "valor": "7500",
        },
    ]


def test_deve_criar_conta_a_pagar_e_receber():
    nova_conta = {"descricao": "Viagem a Rússia", "valor": "15500", "tipo": "PAGAR"}
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 3

    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)

    assert response.status_code == 201
    assert response.json() == nova_conta_copy
