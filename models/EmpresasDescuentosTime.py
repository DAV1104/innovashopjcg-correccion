from config.db import db, ma, app

class EmpresasDescuentosTime(db.Model):
    __tablename__ = "empresas_descuentos_time"
    id = db.Column(db.Integer, primary_key=True)
    porcentaje_descuento = db.Column(db.Float)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'))

    def __init__(self, porcentaje_descuento, fecha_inicio, fecha_fin, empresa_id):
        self.porcentaje_descuento = porcentaje_descuento
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.empresa_id = empresa_id

with app.app_context():
    db.create_all()

class EmpresasDescuentosTimeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'porcentaje_descuento', 'fecha_inicio', 'fecha_fin', 'empresa_id')
