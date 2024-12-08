
from pydantic import BaseModel
from typing import List
from model.atribuicao import Atribuicao

class AtribuicaoSchema(BaseModel):
    """
    Define como uma nova atribuição deve ser representada
    """
    custo_id: int  


class ListagemAtribuicoesSchema(BaseModel):
    """
    Define como uma listagem de atribuições será retornada
    """
    atribuicoes: List[AtribuicaoSchema]


def apresenta_atribuicoes(atribuicoes: List[Atribuicao]):
    """
    Retorna uma representação das atribuições seguindo o schema definido
    """
    result = []
    for atribuicao in atribuicoes:
        result.append({
            "trabalhador_id": atribuicao.trabalhador_id,
            "tarefa_id": atribuicao.tarefa_id,
            "custo": atribuicao.custo_id
        })
    return {"atribuicoes": result}


class AtribuicaoViewSchema(BaseModel):
    """
    Define como uma atribuição será retornada
    """
    id: int = 1
    trabalhador_id: int
    tarefa_id: int
    custo_id: int

class AtribuicaoDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """
    message: str
