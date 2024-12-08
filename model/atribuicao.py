from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from model import Base


class Atribuicao(Base):
    __tablename__ = 'atribuicao'

    id = Column("pk_atribuicao", Integer, primary_key=True)
    custo_id = Column(Integer, ForeignKey('custo.pk_custo', ondelete="CASCADE"), nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())

    custo = relationship("Custo")

    def __init__(self, custo_id: int, data_insercao: datetime = None):
        """
        Cria uma Atribuição

        Arguments:
            custo_id: ID do custo associado à atribuição.
            data_insercao: Data de inserção no banco de dados.
        """
        self.custo_id = custo_id
        if data_insercao:
            self.data_insercao = data_insercao
