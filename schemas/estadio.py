from marshmallow import Schema, fields

class EstadioSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    cidade = fields.Str()
    capacidade = fields.Int()
    inauguracao = fields.Int()
    imagem = fields.Str()

estadio_schema = EstadioSchema()
estadios_schema = EstadioSchema(many=True)
