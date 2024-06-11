from config.db import db, ma, app

class ProductoAlterno(db.Model):
    __tablename__ = "productos_alternos"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    alterno_id = db.Column(db.Integer, db.ForeignKey('productos.id'))

    def __init__(self, producto_id, alterno_id):
        self.producto_id = producto_id
        self.alterno_id = alterno_id

with app.app_context():
    db.create_all()

class ProductoAlternoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'producto_id', 'alterno_id')
