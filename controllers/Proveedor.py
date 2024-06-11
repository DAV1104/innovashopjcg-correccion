# controllers/Proveedor.py
from flask import Blueprint, request, jsonify, session
from config.db import db
from models.Proveedor import Proveedor
from models.Compra import Compra
from .Auth import token_required, empresa_required

ruta_proveedor = Blueprint('proveedor_route', __name__)

@ruta_proveedor.route('/proveedores', methods=['GET'])
def get_proveedores():
    proveedores = Proveedor.query.all()
    proveedores_info = [{"id": proveedor.id, "nombre": proveedor.nombre} for proveedor in proveedores]
    return jsonify(proveedores_info)

@ruta_proveedor.route('/proveedores-list', methods=['GET'])
@token_required
def get_proveedor():
    empresa_id = session.get('empresa_id')
    if not empresa_id:
        return jsonify({"error": "No enterprise in session"}), 400

    compras = Compra.query.filter_by(empresa_id=empresa_id).all()
    if not compras:
        return jsonify({"error": "No purchases found for this enterprise"}), 404

    proveedor_ids = list(set(compra.proveedor_id for compra in compras))
    proveedores = Proveedor.query.filter(Proveedor.id.in_(proveedor_ids)).all()

    proveedores_info = [{
        "id": proveedor.id,
        "nombre": proveedor.nombre,
        "contacto": proveedor.contacto,
        "telefono": proveedor.telefono,
        "direccion": proveedor.direccion
    } for proveedor in proveedores]

    return jsonify(proveedores_info)

@ruta_proveedor.route('/add-proveedor', methods=['POST'])
@token_required
@empresa_required
def add_proveedor():
    data = request.json
    nombre = data.get('nombre')
    contacto = data.get('contacto')
    telefono = data.get('telefono')
    direccion = data.get('direccion')

    existing_proveedor = Proveedor.query.filter_by(nombre=nombre, contacto=contacto).first()
    if existing_proveedor:
        return jsonify({"error": "Proveedor already exists"}), 409

    nuevo_proveedor = Proveedor(
        nombre=nombre,
        contacto=contacto,
        telefono=telefono,
        direccion=direccion
    )
        
    db.session.add(nuevo_proveedor)
    db.session.commit()

    return jsonify({"success": True})
