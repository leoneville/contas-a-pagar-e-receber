from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from shared.dependencies import get_db
from shared.database import Base


client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_deve_listar_contas_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post(
        "/contas-a-pagar-e-receber",
        json={"descricao": "Viagem a Rússia", "valor": 15500.00, "tipo": "PAGAR"},
    )
    client.post(
        "/contas-a-pagar-e-receber",
        json={"descricao": "Salário", "valor": 100000.00, "tipo": "RECEBER"},
    )

    response = client.get("/contas-a-pagar-e-receber")
    assert response.status_code == 200
    assert response.json()["contas"] == [
        {
            "descricao": "Viagem a Rússia",
            "id": 1,
            "tipo": "PAGAR",
            "valor": 15500.00,
        },
        {
            "descricao": "Salário",
            "id": 2,
            "tipo": "RECEBER",
            "valor": 100000.00,
        },
    ]


def test_deve_criar_conta_a_pagar_e_receber():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    nova_conta = {"descricao": "Viagem a Rússia", "valor": 15500.00, "tipo": "PAGAR"}
    nova_conta_copy = nova_conta.copy()
    nova_conta_copy["id"] = 1

    response = client.post("/contas-a-pagar-e-receber", json=nova_conta)

    assert response.status_code == 201
    assert response.json() == nova_conta_copy


def test_deve_retornar_erro_quando_exceder_a_descricao():
    response = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "Assistir o Ceará jogar na argentina pela copa Sulamericana",
            "valor": 10_000.00,
            "tipo": "PAGAR",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "descricao"]


def test_deve_retornar_erro_quando_a_descricao_for_menor_do_que_o_necessario():
    response = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "oi",
            "valor": 10_000.00,
            "tipo": "PAGAR",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "descricao"]


def test_deve_retornar_erro_quando_o_valor_for_zero_ou_menor():
    response = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "Test",
            "valor": 0,
            "tipo": "PAGAR",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "valor"]

    response = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "Test2",
            "valor": -1,
            "tipo": "PAGAR",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "valor"]


def test_deve_retornar_erro_quando_o_tipo_for_invalido():
    response = client.post(
        "/contas-a-pagar-e-receber",
        json={
            "descricao": "Test tipo",
            "valor": 10,
            "tipo": "PAYMENT",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "tipo"]
