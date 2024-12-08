from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

from model import Base


class Especialidade(Base):
    __tablename__ = 'especialidade'

    id = Column("pk_especialidade", Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

    trabalhadores = relationship("TrabalhadorEspecialidade", back_populates="especialidade")

    def __init__(self, nome: str, data_insercao: datetime = None):
        self.nome = nome
        if data_insercao:
            self.data_insercao = data_insercao
