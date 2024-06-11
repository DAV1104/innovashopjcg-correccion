from config.db import db, ma, app
from datetime import datetime

class Compra(db.Model):
    __tablename__ = "compras"
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, nullable=False)
    proveedor_id = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, empresa_id, proveedor_id, fecha=None):
        self.empresa_id = empresa_id
        self.proveedor_id = proveedor_id
        if fecha:
            self.fecha = fecha
        else:
            self.fecha = datetime.utcnow()

with app.app_context():
    db.create_all()

class CompraSchema(ma.Schema):
    class Meta:
        fields = ('id', 'empresa_id', 'proveedor_id', 'fecha')
