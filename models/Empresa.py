from config.db import db, ma, app
from datetime import datetime

class Empresa(db.Model):
    __tablename__ = "empresas"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True)
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    usuario = db.Column(db.String(255), unique=True)
    contraseña = db.Column(db.String(255))
    rol = db.Column(db.String(255), default='empresa')
    nit = db.Column(db.String(255), unique=True)
    session_limit = db.Column(db.Date)
    general_discount = db.Column(db.Float, default=0.0)
    tax = db.Column(db.Float, default=0.0)
    profit_percentage = db.Column(db.Float, default=0.0)
    ultima_sesion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='activo')
    # modulo_clientes = dbColumn(db.Boolean, default=True)
    # modulo_vendedores = dbColumn(db.Boolean, default=True)
    # modulo_porcentajes = dbColumn(db.Boolean, default=True)

    def __init__(self, nombre, direccion, telefono, email, usuario, contraseña, nit, session_limit, general_discount, tax, profit_percentage):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.usuario = usuario
        self.contraseña = contraseña
        self.nit = nit
        self.session_limit = session_limit
        self.general_discount = general_discount
        self.tax = tax
        self.profit_percentage = profit_percentage

with app.app_context():
    db.create_all()

class EmpresaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'direccion', 'telefono', 'email', 'usuario', 'contraseña', 'rol', 'nit', 'session_limit', 'general_discount', 'tax', 'profit_percentage', 'ultima_sesion', 'estado')
