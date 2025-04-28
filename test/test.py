from src.Apitest import *
import pytest

@pytest.fixture
def aluno_teste():
    return {"id": 1001, "nome": "fulanoteste", "turma": "A", "matricula": 111}

def test_carregar_aluno():
    alunos = carregar_aluno()
    assert isinstance(alunos, list)

def test_salvar_aluno(aluno_teste):
    salvar_aluno(aluno_teste)
    alunos = carregar_aluno()
    aluno_encontrado = next((aluno for aluno in alunos if aluno["nome"] == "fulanoteste"), None)
    assert aluno_encontrado is not None

def test_listar_alunos():
    alunos = listar_alunos()
    if isinstance(alunos, dict):
        assert alunos == {"mensagem": "Nenhum Aluno encontrado!!"}
    else:
        assert isinstance(alunos, list)

def test_consultar_alunos():
    resultado = consultar_alunos("id", 1)
    assert resultado[0]["nome"] == "fulanoteste"

    resultado_erro = consultar_alunos("id", "9999")
    assert resultado_erro == {"mensagem": "Aluno não existe ou não encontrado!!"}


def test_incluir_aluno(aluno_teste):
    alunos_existentes = carregar_aluno()

    aluno_existente = next((a for a in alunos_existentes if a["id"] == aluno_teste[0]["id"]), None)
    if aluno_existente:
        alunos_existentes.remove(aluno_existente)
        salvar_aluno(alunos_existentes)

    incluir_aluno(aluno_teste[0])
    alunos = carregar_aluno()
    assert any(a["id"] == aluno_teste[0]["id"] for a in alunos)


def test_alterar_aluno(aluno_teste):
    novo_aluno = Aluno(id=4, nome="Depois", turma="D", matricula=444)

    alterar_aluno("id", "4", novo_aluno)

    alunos = carregar_aluno()

    aluno_alterado = next((a for a in alunos if a["id"] == 4), None)

    assert aluno_alterado["nome"] == "Depois"
    assert aluno_alterado["turma"] == "D"
    assert aluno_alterado["matricula"] == 444




