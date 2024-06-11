from config.db import db, ma, app

class Proveedor(db.Model):
    __tablename__ = "proveedores"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True)
    contacto = db.Column(db.String(255))
    telefono = db.Column(db.String(255))
    direccion = db.Column(db.String(255))

    def __init__(self, nombre, contacto, telefono, direccion):
        self.nombre = nombre
        self.contacto = contacto
        self.telefono = telefono
        self.direccion = direccion

with app.app_context():
    db.create_all()

class ProveedorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'contacto', 'telefono', 'direccion')
