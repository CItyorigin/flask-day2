from marshmallow import Schema, fields

class BookSchema(Schema):
    id = fields.Int(dump_only=True)  # 출력 전용
    title = fields.Str(required=True)
    author = fields.Str(required=True)
