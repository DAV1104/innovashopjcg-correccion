from config.db import db, ma, app

class ClientesEmpresas(db.Model):
    __tablename__ = "clientes_empresas"
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('modulos.id'), nullable=False)

    def __init__(self, empresa_id, usuario_id):
        self.empresa_id = empresa_id
        self.usuario_id = usuario_id

with app.app_context():
    db.create_all()

class ModuloEmpresaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'empresa_id', 'usuario_id')
