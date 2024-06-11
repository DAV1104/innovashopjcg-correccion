from config.db import db, ma, app

class VendedoresEmpresas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_vendedor = db.Column(db.Integer)
    id_empresa = db.Column(db.Integer)
    
    def __init__(self, id_vendedor, id_empresa):
        self.id_vendedor = id_vendedor
        self.id_empresa = id_empresa
        
with app.app_context():
    db.create_all()
    
class VendedoresSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_vendedor', 'id_empresa')