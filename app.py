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
    "headers": [
    ],
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
                descripton: Uma mensagem de boas vindas
        """
        return {"message": "Bem-vindo a pagina da documentação"}

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
                for (chave, valor) in request.form.items():
                    setattr(jogador, chave, valor)
                session.commit()
                return jogador_schema.dump(jogador)
        except Exception as err:
            return {"message": err}

    
api.add_resource(HomeResource, '/')
api.add_resource(JogadorResource, '/jogador/<string:nome>')

