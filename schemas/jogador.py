from marshmallow import Schema, fields

class JogadorSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    altura = fields.Float()
    ano_nascimento = fields.Int()
    posicao = fields.Str()
    peso = fields.Float()
    numero_camisa = fields.Int()
    perna_preferida = fields.Str()
    jogos_disputados = fields.Int()
    gols_marcados = fields.Int()
    assistencias = fields.Int()
    imagem = fields.Str()

jogador_schema = JogadorSchema()
jogadores_schema = JogadorSchema(many=True)