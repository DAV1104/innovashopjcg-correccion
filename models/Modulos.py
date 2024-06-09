from config.db import db, ma, app

class Modulo(db.Model):
    __tablename__ = "modulos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

with app.app_context():
    db.create_all()

class ModuloSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'descripcion')
