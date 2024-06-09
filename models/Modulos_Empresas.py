from config.db import db, ma, app

class ModuloEmpresa(db.Model):
    __tablename__ = "modulosempresas"
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulos.id'), nullable=False)
    estado = db.Column(db.Boolean, default=False)

    def __init__(self, empresa_id, modulo_id, estado=False):
        self.empresa_id = empresa_id
        self.modulo_id = modulo_id
        self.estado = estado

with app.app_context():
    db.create_all()

class ModuloEmpresaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'empresa_id', 'modulo_id', 'estado')
