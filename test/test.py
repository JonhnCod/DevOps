from fastapi.testclient import TestClient
from src.Apitest import app  # Importe a instância do FastAPI
import pytest
import json

client = TestClient(app)

def get_aluno_teste_data():
    return {"id": 1001, "nome": "fulanoteste", "turma": "A", "matricula": 123}

def clear_alunos_data():
    """Limpa os dados de alunos para garantir testes isolados."""
    with open('src/alunos.json', 'w') as f:
        json.dump([], f, indent=4)

@pytest.fixture(scope="function", autouse=True)
def setup_teardown():
    """Fixture para limpar os dados antes de cada teste."""
    clear_alunos_data()
    yield
    clear_alunos_data()

@pytest.fixture
def aluno_teste():
    """Fixture para fornecer um objeto de aluno de teste."""
    return get_aluno_teste_data()

def test_listar_alunos_vazio():
    response = client.get("/alunos/listar")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "Nenhum Aluno encontrado!!"}

def test_listar_alunos_com_dados(aluno_teste):
    client.post("/alunos/incluir/", json=aluno_teste)
    response = client.get("/alunos/listar")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0] == aluno_teste

def test_consultar_alunos_existente(aluno_teste):
    client.post("/alunos/incluir/", json=aluno_teste)
    response = client.get(f"/alunos/consultar/id/{aluno_teste['id']}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0] == aluno_teste

def test_consultar_alunos_nao_existente():
    response = client.get("/alunos/consultar/matricula/9999")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "Aluno não existe ou não encontrado!!"}

def test_incluir_aluno(aluno_teste):
    response = client.post("/alunos/incluir/", json=aluno_teste)
    assert response.status_code == 200
    assert response.json() == {"messagem": "Aluno adicionado com sucesso!!"}
    response_get = client.get("/alunos/listar")
    assert len(response_get.json()) == 1
    assert response_get.json()[0] == aluno_teste

def test_alterar_aluno_existente(aluno_teste):
    client.post("/alunos/incluir/", json=aluno_teste)
    aluno_atualizado = {"id": aluno_teste["id"], "nome": "Depois", "turma": "D", "matricula": 444}
    response = client.put(f"/alunos/alterar/id/{aluno_teste['id']}", json=aluno_atualizado)
    assert response.status_code == 200
    assert response.json()["message"] == "Aluno Alterado"
    assert response.json()["aluno"] == aluno_atualizado
    response_get = client.get(f"/alunos/consultar/id/{aluno_teste['id']}")
    assert response_get.json()[0] == aluno_atualizado

def test_alterar_aluno_nao_existente():
    aluno_atualizado = {"id": 555, "nome": "Outro Nome", "turma": "Y", "matricula": 5555}
    response = client.put("/alunos/alterar/matricula/5555", json=aluno_atualizado)
    assert response.status_code == 200
    assert response.json() == {"message": "Aluno não encontrado."}

def test_deletar_aluno_existente(aluno_teste):
    client.post("/alunos/incluir/", json=aluno_teste)
    response = client.delete(f"/alunos/excluir/id/{aluno_teste['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Aluno deletado com sucesso!"
    assert response.json()["aluno"] == aluno_teste
    response_get = client.get("/alunos/listar")
    assert len(response_get.json()) == 0

def test_deletar_aluno_nao_existente():
    response = client.delete("/alunos/excluir/nome/AlunoInexistente")
    assert response.status_code == 200
    assert response.json() == {'messagem': "Aluno nao encontrado"}



