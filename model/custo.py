from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from model import Base


class Custo(Base):
    __tablename__ = 'custo'

    id = Column("pk_custo", Integer, primary_key=True)
    trabalhador_id = Column(Integer, ForeignKey('trabalhador.pk_trabalhador', ondelete="CASCADE"), nullable=False)
    tarefa_id = Column(Integer, ForeignKey('tarefa.pk_tarefa', ondelete="CASCADE"), nullable=False)
    custo = Column(Float, nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())

    trabalhador = relationship("Trabalhador", back_populates="custos")
    tarefa = relationship("Tarefa", back_populates="custos")

    def __init__(self, trabalhador_id: int, tarefa_id: int, custo: float, data_insercao: datetime = None):
        self.trabalhador_id = trabalhador_id
        self.tarefa_id = tarefa_id
        self.custo = custo
        if data_insercao:
            self.data_insercao = data_insercao
