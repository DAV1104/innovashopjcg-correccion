from config.db import db, ma, app

class CompraDetalles(db.Model):
    __tablename__ = "compra_detalles"
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, nullable=False)
    producto_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_total = db.Column(db.Float, nullable=False)

    def __init__(self, compra_id, producto_id, cantidad, precio_total):
        self.compra_id = compra_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_total = precio_total

with app.app_context():
    db.create_all()

class CompraDetallesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'compra_id', 'producto_id', 'cantidad', 'precio_total')