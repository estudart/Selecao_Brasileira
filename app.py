from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
from flask_cors import CORS
from model import *
from schemas import *

app = Flask(__name__)
CORS(app)
api = Api(app)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "title": "Copa 2002 API",
}

swagger = Swagger(app, config=swagger_config)

class HomeResource(Resource):
    def get(self):
        """
        Bem-vindo à DocPage!

        ---
        tags:
            - nome: Bem-vindo!
        responses:
            200:
                description: Uma mensagem de boas vindas
        """
        return {"message": "Bem-vindo a pagina da documentação"}

class JogadoresResource(Resource):
    def post(self):
        """
        Rota para fazer o post de um jogador através de seu nome.
        
        ---
        tags:
            - Jogador
        parameters:
            - name: nome
              in: formData
              type: string
              required: true
              description: Nome do jogador
            - name: altura
              in: formData
              type: float
              required: true
              description: Altura do jogador.
            - name: ano_nascimento
              in: formData
              type: integer
              required: true
              description: Ano de nascimento do jogador.
            - name: posicao
              in: formData
              type: string
              required: true
              description: Posição do jogador.
            - name: peso
              in: formData
              type: float
              required: true
              description: Peso do jogador.
            - name: numero_camisa
              in: formData
              type: integer
              required: true
              description: Número da camisa do jogador.
            - name: perna_preferida
              in: formData
              type: string
              required: true
              description: Perna preferida do jogador.
            - name: jogos_disputados
              in: formData
              type: integer
              required: true
              description: Número de jogos disputados pelo jogador.
            - name: gols_marcados
              in: formData
              type: integer
              required: true
              description: Número de gols marcados pelo jogador.
            - name: assistencias
              in: formData
              type: integer
              required: true
              description: Número de assistências feitas pelo jogador.
            - name: descricao
              in: formData
              type: string
              required: true
              description: Descricao do jogador.
            - name: imagem
              in: formData
              type: string
              required: false
              description: Imagem do jogador.

        responses:
            200:
                description: Jogador encontrado!
            404:
                description: Jogador não encontrado na base.
        """
        try:
            json_data = request.form
            session = Session()
            novo_jogador_data = jogador_schema.dump(json_data)
            novo_jogador = Jogador(**novo_jogador_data)
            session.add(novo_jogador)
            session.commit()
            return jogador_schema.dump(novo_jogador_data)
        except Exception as err:
            return {"message": err}

class JogadorResource(Resource):
    def get(self, nome):
        """
        Rota para fazer o request de um jogador através de seu nome.
        
        ---
        tags:
            - Jogador
        parameters:
            - name: nome
              in: path
              type: string
              required: true
              description: Nome do jogador
        responses:
            200:
                description: Jogador encontrado!
        """
        try:
            session = Session()
            jogador = session.query(Jogador).filter(Jogador.nome == nome).first()

            if not jogador:
                return {"message": "Jogador não encontrado na base"}
            else:
                return jogador_schema.dump(jogador)
        except Exception as err:
            return {"message": err}
        
    def delete(self, nome):
        """
        Rota para fazer o delete de um jogador através de seu nome.
        
        ---
        tags:
            - Jogador
        parameters:
            - name: nome
              in: path
              type: string
              required: true
              description: Nome do jogador
        responses:
            200:
                description: Jogador encontrado!
        """
        try:
            session = Session()
            jogador = session.query(Jogador).filter(Jogador.nome == nome).first()

            if not jogador:
                return {"message": "Jogador não encontrado na base"}
            else:
                session.query(Jogador).filter(Jogador.nome == nome).delete()
                session.commit()
                return jogador_schema.dump(jogador)
        except Exception as err:
            return {"message": err}
        
    def put(self, nome):
        """
        Rota para fazer o put de um jogador através de seu nome.
        
        ---
        tags:
            - Jogador
        parameters:
            - name: nome
              in: path
              type: string
              required: true
              description: Nome do jogador
            - name: altura
              in: formData
              type: float
              required: false
              description: Altura do jogador.
            - name: ano_nascimento
              in: formData
              type: integer
              required: false
              description: Ano de nascimento do jogador.
            - name: posicao
              in: formData
              type: string
              required: false
              description: Posição do jogador.
            - name: peso
              in: formData
              type: float
              required: false
              description: Peso do jogador.
            - name: numero_camisa
              in: formData
              type: integer
              required: false
              description: Número da camisa do jogador.
            - name: perna_preferida
              in: formData
              type: string
              required: false
              description: Perna preferida do jogador.
            - name: jogos_disputados
              in: formData
              type: integer
              required: false
              description: Número de jogos disputados pelo jogador.
            - name: gols_marcados
              in: formData
              type: integer
              required: false
              description: Número de gols marcados pelo jogador.
            - name: assistencias
              in: formData
              type: integer
              required: false
              description: Número de assistências feitas pelo jogador.
            - name: descricao
              in: formData
              type: string
              required: false
              description: Descricao do jogador.

        responses:
            200:
                description: Jogador encontrado!
            404:
                description: Jogador não encontrado na base.
        """
        try:
            session = Session()
            jogador = session.query(Jogador).filter(Jogador.nome == nome).first()

            if not jogador:
                return {"message": "Jogador não encontrado na base"}
            else:
                for (chave, valor) in request.form.items():
                    setattr(jogador, chave, valor)
                session.commit()
                return jogador_schema.dump(jogador)
        except Exception as err:
            return {"message": err}

class EstadiosResource(Resource):
    def get(self):
        """
        Rota para fazer o request de todos os estadios na base

        ---
        tags:
            - Estadio
        responses:
            200:
                Estadio encontrados com sucesso
        """
        session = Session()
        estadios_data = session.query(Estadio).all()
        json_response = estadios_schema.dump(estadios_data)
        return json_response

    def post(self):
        """
        Rota para fazer o post de um estadio através de seu nome.
        
        ---
        tags:
            - Estadio
        parameters:
            - name: nome
              in: path
              type: string
              required: true
              description: Nome do estadio
            - name: cidade
              in: formData
              type: string
              required: true
              description: Cidade do estadio
            - name: capacidade
              in: formData
              type: integer
              required: true
              description: Capacidade do estadio
            - name: inauguracao
              in: formData
              type: integer
              required: true
              description: Data de inauguração do estadio
            - name: descricao
              in: formData
              type: string
              required: true
              description: Descricao do estadio
            - name: imagem
              in: formData
              type: string
              required: true
              description: Imagem do estadio.

        responses:
            200:
                description: Estadio encontrado!
            404:
                description: Estadio não encontrado na base.
        """
        try:
            json_data = request.form
            session = Session()
            novo_estadio_data = estadio_schema.dump(json_data)
            novo_estadio = Estadio(**novo_estadio_data)
            session.add(novo_estadio)
            session.commit()
            return estadio_schema.dump(novo_estadio_data)
        except Exception as err:
            return {"message": err}

class EstadioResource(Resource):
    def get(self, nome):
        """
        Rota para fazer o request de um estadio através de seu nome.
        
        ---
        tags:
            - Estadio
        parameters:
            - name: nome
              in: path
              type: string
              required: true
              description: Nome do estádio
        responses:
            200:
                description: Jogador encontrado!
        """
        try:
            session = Session()
            estadio = session.query(Estadio).filter(Estadio.nome == nome).first()

            if not estadio:
                return {"message": "Estadio não encontrado na base"}
            else:
                return estadio_schema.dump(estadio)
        except Exception as err:
            return {"message": err}
        
    def delete(self, nome):
        """
        Rota para fazer o delete de um estadio através de seu nome.
        
        ---
        tags:
            - Estadio
        parameters:
            - name: nome
              in: path
              type: string
              required: true
              description: Nome do estadio
        responses:
            200:
                description: Estadio encontrado!
        """
        try:
            session = Session()
            estadio = session.query(Estadio).filter(Estadio.nome == nome).first()

            if not estadio:
                return {"message": "Estadio não encontrado na base"}
            else:
                session.query(Estadio).filter(Estadio.nome == nome).delete()
                session.commit()
                return estadio_schema.dump(estadio)
        except Exception as err:
            return {"message": err}
        
    def put(self, nome):
        """
        Rota para fazer o put de um estadio através de seu nome.
        
        ---
        tags:
            - Estadio
        parameters:
            - name: nome
              in: path
              type: string
              required: true
              description: Nome do estadio
            - name: cidade
              in: formData
              type: string
              required: false
              description: Cidade do estadio
            - name: capacidade
              in: formData
              type: integer
              required: false
              description: Capacidade do estadio
            - name: inauguracao
              in: formData
              type: integer
              required: false
              description: Data de inauguração do estadio
            - name: descricao
              in: formData
              type: string
              required: false
              description: Descricao do estadio
            - name: imagem
              in: formData
              type: string
              required: false
              description: Imagem do estadio.

        responses:
            200:
                description: Estadio encontrado!
            404:
                description: Estadio não encontrado na base.
        """
        try:
            session = Session()
            estadio = session.query(Estadio).filter(Estadio.nome == nome).first()

            if not estadio:
                return {"message": "Estadio não encontrado na base"}
            else:
                for (chave, valor) in request.form.items():
                    setattr(estadio, chave, valor)
                session.commit()
                return estadio_schema.dump(estadio)
        except Exception as err:
            return {"message": err}


class CriaJogadores(Resource):
    def get(self):
        jogador1 = {
            "nome": "Ronaldinho Gaúcho",
            "altura": 1.81,
            "ano_nascimento": 1980,
            "posicao": "meia",
            "peso": "80.5",
            "numero_camisa": 11,
            "perna_preferida": "Ambidestro",
            "jogos_disputados": 5,
            "gols_marcados": 2,
            "assistencias": 3,
            "descricao": "Esse jogador...",
            "imagem": "https://alemdoplacar.files.wordpress.com/2011/05/pit5.jpeg"
            }
        
        jogador2 = {
            "nome": "Marcos",
            "altura": 1.88,
            "ano_nascimento": 1973,
            "posicao": "goleiro",
            "peso": 88.0,
            "numero_camisa": 1,
            "perna_preferida": "Destro",
            "jogos_disputados": 7,
            "gols_marcados": 0,
            "assistencias": 4,
            "descricao": "Esse jogador...",
            "imagem": "https://down-br.img.susercontent.com/file/sg-11134201-22110-ip9t48pkh8jv0a"
            }
        
        jogador3 = {
            "nome": "Cafu",
            "altura": 1.76,
            "ano_nascimento": 1970,
            "posicao": "lateral_direito",
            "peso": 72.0,
            "numero_camisa": 2,
            "perna_preferida": "Destro",
            "jogos_disputados": 7,
            "gols_marcados": 0,
            "assistencias": 1,
            "descricao": "Esse jogador...",
            "imagem": "https://conteudo.imguol.com.br/2012/03/27/cafu-levanta-a-copa-do-mundo-pela-selecao-brasileira-em-2002-1332902990448_450x600.jpg"
            }
        
        jogador4 = {
            "nome": "Lucio",
            "altura": 1.88,
            "ano_nascimento": 1978,
            "posicao": "zagueiro",
            "peso": 84.0,
            "numero_camisa": 3,
            "perna_preferida": "Destro",
            "jogos_disputados": 7,
            "gols_marcados": 1,
            "assistencias": 0,
            "descricao": "Esse jogador...",
            "imagem": "https://i.pinimg.com/736x/ee/0e/89/ee0e89f31d6bb6fcd730f07758faf903.jpg"
            }
        
        session = Session()
        session.add(Jogador(**jogador1))
        session.add(Jogador(**jogador2))
        session.add(Jogador(**jogador3))
        session.add(Jogador(**jogador4))

        session.commit()

        return {"message": "Jogadores criados na base"}
    
class CriaEstadios(Resource):
    def get(self): 
        estadio2 = {
            "nome": "Estádio Internacional de Yokohama",
            "cidade": "Yokohama",
            "capacidade": 72000,
            "inauguracao": 1998,
            "descricao": "Esse estadio...",
            "imagem": "https://miro.medium.com/v2/resize:fit:3000/1*Y3_0mVDGp-p2RRFalkXfkg.jpeg"
            }
        
        estadio3 = {
            "nome": "Estádio de Suwon",
            "cidade": "Suwon",
            "capacidade": 43830,
            "inauguracao": 2001,
            "descricao": "Esse estadio...",
            "imagem": "https://i.pinimg.com/originals/d2/8c/1e/d28c1e823127c7225c3c24d96f98ae55.jpg"
            }
        
        estadio4 = {
            "nome": "Estádio de Incheon",
            "cidade": "Incheon",
            "capacidade": 52500,
            "inauguracao": 2001,
            "descricao": "Esse estadio...",
            "imagem": "https://i.pinimg.com/originals/bf/98/d6/bf98d67b79529ab869e3f95adad9cdae.jpg"
            }
        
        estadio5 = {
            "nome": "Estádio de Seogwipo",
            "cidade": "Seogwipo",
            "capacidade": 42477,
            "inauguracao": 2001,
            "descricao": "Esse estadio...",
            "imagem": "https://trivela.com.br/wp-content/uploads/2014/05/Copa-2002_Est%C3%A1dio-Jeju.jpg"
        }
        
        session = Session()
        session.add(Estadio(**estadio2))
        session.add(Estadio(**estadio3))
        session.add(Estadio(**estadio4))
        session.add(Estadio(**estadio5))

        session.commit()

        return {"message": "Estadios criados na base"}

api.add_resource(HomeResource, '/')
api.add_resource(JogadorResource, '/jogador/<string:nome>')
api.add_resource(JogadoresResource, '/jogador')
api.add_resource(CriaJogadores, '/cria_jogadores')
api.add_resource(CriaEstadios, '/cria_estadios')
