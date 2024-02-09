from sqlalchemy import Float, Integer, String, Column
from model import Base

class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    altura = Column(Float)
    ano_nascimento = Column(Integer)
    posicao = Column(String)
    peso = Column(Float)
    numero_camisa = Column(Integer)
    perna_preferida = Column(String)
    jogos_disputados = Column(Integer)
    gols_marcados = Column(Integer)
    assistencias = Column(Integer)
    descricao = Column(String)
    imagem = Column(String)