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

api.add_resource(HomeResource, '/')
api.add_resource(JogadorResource, '/jogador/<string:nome>')
api.add_resource(JogadoresResource, '/jogador')
