from marshmallow import Schema, fields

class TecnicoSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    altura = fields.Float()
    ano_nascimento = fields.Int()
    descricao = fields.Str()
    imagem = fields.Str()

tecnico_schema = TecnicoSchema()