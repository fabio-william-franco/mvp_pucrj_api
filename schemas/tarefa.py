from pydantic import BaseModel
from typing import List, Optional
from model.tarefa import Tarefa


class TarefaSchema(BaseModel):
    """
    Define como uma nova tarefa deve ser representada
    """
    nome: str = "Tarefa X"
    especialidade_id: int


class TarefaBuscaSchema(BaseModel):
    """
    Define como deve ser a estrutura que representa a busca de uma tarefa
    """
    nome: str


class ListagemTarefasSchema(BaseModel):
    """
    Define como uma listagem de tarefas será retornada
    """
    tarefas: List[TarefaSchema]


def apresenta_tarefas(tarefas: List[Tarefa]):
    """
    Retorna uma representação das tarefas seguindo o schema definido
    """
    result = []
    for tarefa in tarefas:
        especialidade = tarefa.especialidade  
        result.append({
            "id": tarefa.id,
            "nome": tarefa.nome,
            "especialidade": {
                "id": especialidade.id,
                "nome": especialidade.nome
            }
        })
    return {"tarefas": result}


class EspecialidadeSchema(BaseModel):
    """
    Define como uma especialidade será representada
    """
    id: int
    nome: str
    
class TarefaViewSchema(BaseModel):
    """
    Define como uma tarefa será retornada
    """
    id: int
    nome: str
    especialidade: EspecialidadeSchema  



class TarefaDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """
    message: str
    nome: str



