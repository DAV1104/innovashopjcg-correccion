from config.db import db, app

class InformesModulos(db.Model):
    __tablename__ = "informes_modulos"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer)
    tipo_informe = db.Column(db.String(255))  # 'General' or 'Mensual'
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, producto_id, tipo_informe):
        self.producto_id = producto_id
        self.tipo_informe = tipo_informe

with app.app_context():
    db.create_all()
