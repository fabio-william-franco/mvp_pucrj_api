from pydantic import BaseModel
from typing import List, Optional
from model.especialidade import Especialidade

class EspecialidadeSchema(BaseModel):
    """
    Define como uma nova especialidade deve ser representada
    """
    nome: str = "Especialidade X"


class ListagemEspecialidadesSchema(BaseModel):
    """
    Define como uma listagem de especialidades será retornada
    """
    especialidades: List[dict]  


def apresenta_especialidades(especialidades: List[Especialidade]):
    """
    Retorna uma representação das especialidades com id e nome.
    """
    return {
        "especialidades": [
            {"id": especialidade.id, "nome": especialidade.nome}
            for especialidade in especialidades
        ]
    }



class EspecialidadeViewSchema(BaseModel):
    """
    Define como uma especialidade será retornada
    """
    id: int
    nome: str
    trabalhadores: List[dict]  


class EspecialidadeDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """
    message: str
    nome: str
