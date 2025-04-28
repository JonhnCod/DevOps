from src.Apitest import *
import pytest
import asyncio




@pytest.mark.asyncio
async def test_listar_alunos():
    alunos = await listar_alunos()  # Usar await para esperar a função assíncrona
    if isinstance(alunos, dict):
        assert alunos == {"mensagem": "Nenhum Aluno encontrado!!"}
    else:
        assert isinstance(alunos, list)


@pytest.mark.asyncio
async def test_consultar_alunos():
    resultado = await consultar_alunos("id", "1001")  # Usar await aqui também
    assert resultado[0]["nome"] == "fulanoteste"


@pytest.mark.asyncio
async def test_incluir_aluno(aluno_teste):
    alunos_existentes = await carregar_aluno()  # Esperar pela função assíncrona

    # Remover aluno se já existir
    aluno_existente = next((a for a in alunos_existentes if a["id"] == aluno_teste["id"]), None)
    if aluno_existente:
        alunos_existentes.remove(aluno_existente)
        await salvar_aluno(alunos_existentes)  # Esperar pela função assíncrona

    # Incluir aluno
    await incluir_aluno(aluno_teste)  # Esperar pela função assíncrona
    alunos = await carregar_aluno()  # Esperar pela função assíncrona
    assert any(a["id"] == aluno_teste["id"] for a in alunos)


@pytest.mark.asyncio
async def test_alterar_aluno(aluno_teste):
    novo_aluno = Aluno(id=1001, nome="Depois", turma="D", matricula=444)

    # Alterar aluno existente
    await alterar_aluno("id", "1001", novo_aluno)  # Esperar pela função assíncrona

    alunos = await carregar_aluno()  # Esperar pela função assíncrona

    aluno_alterado = next((a for a in alunos if a["id"] == 1001), None)

    assert aluno_alterado["nome"] == "Depois"




