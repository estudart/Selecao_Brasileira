from marshmallow import Schema, fields

class TecnicoSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    altura = fields.Float()
    ano_nascimento = fields.Int()
    imagem = fields.Str()

tecnico_schema = TecnicoSchema()