from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_empresa():
    response = client.post(
        "/empresas/",
        json={
            "nome": "Empresa Teste",
            "cnpj": "12345678901234",
            "endereco": "Rua Teste, 123",
            "email": "teste@empresa.com",
            "telefone": "11999999999"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Empresa Teste"
    assert "id" in data

def test_read_empresa():
    response = client.get("/empresas/1")
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Empresa Teste"

def test_create_obrigacao():
    response = client.post(
        "/obrigacoes/?empresa_id=1",
        json={
            "nome": "Obrigação Teste",
            "periodicidade": "mensal"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Obrigação Teste"
    assert "id" in data