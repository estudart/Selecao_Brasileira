from sqlalchemy import Float, Integer, String, Column
from model import Base


class Tecnico(Base):
    __tablename__ = 'tecnicos'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    altura = Column(Float)
    ano_nascimento = Column(Integer)
    descricao = Column(String)
    imagem = Column(String)