from config.db import db, ma, app

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    apellidos = db.Column(db.String(255))
    telefono = db.Column(db.String(255))
    email = db.Column(db.String(255))
    cedula = db.Column(db.String(255))
    usuario = db.Column(db.String(255))
    contraseña = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    rol = db.Column(db.String(255))  # New role column

    def __init__(self, nombre, apellidos, telefono, email, cedula, usuario, contraseña, direccion, rol):
        self.nombre = nombre
        self.apellidos = apellidos
        self.telefono = telefono
        self.email = email
        self.cedula = cedula
        self.usuario = usuario
        self.contraseña = contraseña
        self.direccion = direccion
        self.rol = rol

with app.app_context():
    db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'apellidos', 'telefono', 'email', 'cedula', 'usuario', 'contraseña', 'direccion', 'rol')
