from pydantic import BaseModel
from typing import List, Optional
from model.trabalhador import Trabalhador

from pydantic import BaseModel
from typing import List

class TrabalhadorSchema(BaseModel):
    """
    Define o schema para editar ou criar um trabalhador.
    """
    nome: str  
    especialidades_nomes: List[str]  


class TrabalhadorBuscaSchema(BaseModel):
    """
    Define como deve ser a estrutura que representa a busca de um trabalhador
    """
    nome: Optional[str] = None


class ListagemTrabalhadoresSchema(BaseModel):
    """
    Define como uma listagem de trabalhadores será retornada
    """
    trabalhadores: List[dict]  


def apresenta_trabalhadores(trabalhadores: List[Trabalhador]):
    """
    Retorna uma representação dos trabalhadores seguindo o schema definido
    """
    result = []
    for trabalhador in trabalhadores:
        especialidades = [
            {"id": te.especialidade.id, "nome": te.especialidade.nome}
            for te in trabalhador.especialidades
        ]
        result.append({
            "id": trabalhador.id,
            "nome": trabalhador.nome,
            "especialidades": especialidades
        })
    return {"trabalhadores": result}


class TrabalhadorViewSchema(BaseModel):
    """
    Define como um trabalhador será retornado
    """
    id: int
    nome: str
    especialidades: List[dict]  


class TrabalhadorDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """
    message: str
    nome: str
