from sqlalchemy import Float, Integer, String, Column
from model import Base

class Estadio(Base):
    __tablename__ = 'estadios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cidade = Column(String)
    capacidade = Column(Integer)
    inauguracao = Column(Integer)
    imagem = Column(String)