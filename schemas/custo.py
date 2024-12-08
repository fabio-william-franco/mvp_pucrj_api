from pydantic import BaseModel
from typing import List
from model.custo import Custo

class CustoSchema(BaseModel):
    """
    Define como um custo deve ser representado
    """
    trabalhador_id: int
    tarefa_id: int
    custo: float = 100.0


class ListagemCustosSchema(BaseModel):
    """
    Define como uma listagem de custos será retornada
    """
    custos: List[CustoSchema]


def apresenta_custos(custos: List[Custo]):
    """
    Retorna uma representação dos custos seguindo o schema definido
    """
    result = []
    for custo in custos:
        result.append({
            "trabalhador_id": custo.trabalhador_id,
            "tarefa_id": custo.tarefa_id,
            "custo": custo.custo
        })
    return {"custos": result}


class CustoViewSchema(BaseModel):
    """
    Define como um custo será retornado
    """
    id: int
    trabalhador: str
    tarefa: str
    custo: float


class CustoDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """
    message: str
    id: int

class CustoIdSchema(BaseModel):
    """
    Define o esquema da requisição para deletar um custo
    pelo ID.
    """
    id: int
