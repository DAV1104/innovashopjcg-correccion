from config.db import db, ma, app
from datetime import datetime

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float)  # Cost price
    precio_venta = db.Column(db.Float)  # Selling price
    existencias = db.Column(db.Integer)
    min_existencias = db.Column(db.Integer)
    img_src = db.Column(db.String(255))

    def __init__(self, nombre, descripcion, precio, precio_venta, existencias, min_existencias, img_src):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.precio_venta = precio_venta
        self.existencias = existencias
        self.min_existencias = min_existencias
        self.img_src = img_src

with app.app_context():
    db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'descripcion', 'precio', 'precio_venta', 'existencias', 'min_existencias', 'img_src')
