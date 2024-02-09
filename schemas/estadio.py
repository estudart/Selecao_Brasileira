from marshmallow import Schema, fields

class EstadioSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    cidade = fields.Str()
    capacidade = fields.Int()
    inauguracao = fields.Int()
    descricao = fields.Str()
    imagem = fields.Str()

estadio_schema = EstadioSchema()
estadios_schema = EstadioSchema(many=True)
