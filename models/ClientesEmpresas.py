from config.db import db, ma, app

class ClientesEmpresas(db.Model):
    __tablename__ = "clientes_empresas"
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    

with app.app_context():
    db.create_all()

class ClientesEmpresasSchema(ma.Schema):
    class Meta:
        fields = ('id', 'empresa_id', 'usuario_id')