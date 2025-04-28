from fastapi import FastAPI
import json
from pydantic import BaseModel

app = FastAPI()

def carregar_aluno():
    with open('src/alunos.json', 'r') as file:
        return json.load(file)

def salvar_aluno(aluno):
    with open('src/alunos.json', 'w') as file:
        json.dump(aluno, file, indent=4)

class Aluno(BaseModel):
    id: int = None
    nome: str = None
    turma: str = None
    matricula: int = None


@app.get("/alunos/listar")
async def listar_alunos():
    alunos = carregar_aluno()
    if len(alunos) < 1:
        return {"mensagem":"Nenhum Aluno encontrado!!"}
    else:
        return alunos


@app.get("/alunos/consultar/{campo}/{valor}")
async def consultar_alunos(campo: str, valor: str):
    alunos = carregar_aluno()

    if campo in ["id", "matricula"]:
        valor = int(valor)

    resultado = [aluno for aluno in alunos if aluno.get(campo) == valor]

    if len(resultado) < 1:
        return {"mensagem": "Aluno não existe ou não encontrado!!"}
    else:
        return resultado

@app.post("/alunos/incluir/")
async def incluir_aluno(aluno: Aluno):
    alunos = carregar_aluno()
    novo_aluno = aluno.dict()
    alunos.append(novo_aluno)
    salvar_aluno(alunos)
    return {"messagem": "Aluno adicionado com sucesso!!"}


@app.delete("/alunos/excluir/{campo}/{valor}")
async def deletar_aluno(campo: str, valor: str):

    alunos = carregar_aluno()

    if campo == "id" or campo == "matricula":
        valor = int(valor)

    aluno_deletado = next((aluno for aluno in alunos if aluno.get(campo) == valor), False)

    if not aluno_deletado:
        return {'messagem': "Aluno nao encontrado"}

    alunos = [aluno for aluno in alunos if aluno.get(campo) != valor]
    salvar_aluno(alunos)

    return {
        "message": "Aluno deletado com sucesso!",
        "aluno": aluno_deletado
    }


@app.put("/alunos/alterar/{campo}/{valor}")
async def alterar_aluno(campo: str, valor: str, aluno_atualizado: Aluno):
    if campo == "id" or campo == "matricula":
        valor = int(valor)

    alunos = carregar_aluno()

    aluno_encontrado = next((aluno for aluno in alunos if aluno.get(campo) == valor), False)

    if not aluno_encontrado:
        return {"message":"Aluno não encontrado."}

    for i, aluno in enumerate(alunos):
        if aluno.get(campo) == valor:
            alunos[i] = aluno_atualizado.dict()
            break

    salvar_aluno(alunos)

    return {
        "message": "Aluno Alterado",
        "aluno": aluno_atualizado
    }






