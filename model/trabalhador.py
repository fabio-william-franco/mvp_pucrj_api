from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from model import Base

class Trabalhador(Base):
    __tablename__ = 'trabalhador'
    id = Column("pk_trabalhador", Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())
    
    especialidades = relationship("TrabalhadorEspecialidade", back_populates="trabalhador", cascade="all, delete-orphan")
    custos = relationship("Custo", back_populates="trabalhador")

    def __init__(self, nome: str, data_insercao: datetime = None):
        self.nome = nome
        if data_insercao:
            self.data_insercao = data_insercao