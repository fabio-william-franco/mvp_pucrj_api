from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from model import Base


class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column("pk_tarefa", Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)
    especialidade_id = Column(Integer, ForeignKey('especialidade.pk_especialidade'), nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())

    especialidade = relationship("Especialidade")
    custos = relationship("Custo", back_populates="tarefa")

    def __init__(self, nome: str, especialidade_id: int, data_insercao: datetime = None):
        self.nome = nome
        self.especialidade_id = especialidade_id
        if data_insercao:
            self.data_insercao = data_insercao
