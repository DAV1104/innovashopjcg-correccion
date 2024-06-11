from config.db import db, ma, app

class CotizacionEmpresaDetalles(db.Model):
    __tablename__ = "cotizacion_empresa_detalles"
    id = db.Column(db.Integer, primary_key=True)
    cotizacion_id = db.Column(db.Integer, nullable=False)
    producto_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_total = db.Column(db.Float, nullable=False)

    def __init__(self, cotizacion_id, producto_id, cantidad, precio_total):
        self.cotizacion_id = cotizacion_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_total = precio_total

with app.app_context():
    db.create_all()

class CotizacionEmpresaDetallesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'cotizacion_id', 'producto_id', 'cantidad', 'precio_total')