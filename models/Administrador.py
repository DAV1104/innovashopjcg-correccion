from config.db import db, ma, app

class Administrador(db.Model):
    __tablename__ = 'administradores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    usuario = db.Column(db.String(255))
    contraseña = db.Column(db.String(255))
    
    def __init__(self, nombre, usuario, contraseña):
        self.nombre = nombre
        self.usuario = usuario
        self.contraseña = contraseña
    
        
with app.app_context():
    db.create_all()
    
class AdministradorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'usuario', 'contraseña')