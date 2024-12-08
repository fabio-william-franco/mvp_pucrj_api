from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from model import Base

class TrabalhadorEspecialidade(Base):
    __tablename__ = 'trabalhador_especialidade'
    id = Column("pk_trabalhador_especialidade", Integer, primary_key=True)
    trabalhador_id = Column(Integer, ForeignKey('trabalhador.pk_trabalhador', ondelete="CASCADE"), nullable=False)
    especialidade_id = Column(Integer, ForeignKey('especialidade.pk_especialidade', ondelete="CASCADE"), nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())
    
    trabalhador = relationship("Trabalhador", back_populates="especialidades")
    especialidade = relationship("Especialidade", back_populates="trabalhadores")

    def __init__(self, trabalhador_id: int, especialidade_id: int, data_insercao: datetime = None):
        self.trabalhador_id = trabalhador_id
        self.especialidade_id = especialidade_id
        if data_insercao:
            self.data_insercao = data_insercao