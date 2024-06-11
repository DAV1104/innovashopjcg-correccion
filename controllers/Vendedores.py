from flask import Blueprint, jsonify, session, request
from config.db import db
from .Auth import token_required
from models.VendedoresEmpresas import VendedoresEmpresas
from models.Usuario import Usuario# Adjust the import as per your project structure

ruta_vendedor = Blueprint('ruta_vendedor', __name__)

@ruta_vendedor.route('/vendedores', methods=['GET'])
@token_required
def get_vendedores():
    empresa_id = session.get('empresa_id')
    if not empresa_id:
        return jsonify({"error": "No enterprise in session"}), 400

    # Query VendedoresEmpresas to get vendedor_ids
    vendedores_empresas = VendedoresEmpresas.query.filter_by(id_empresa=empresa_id).all()
    vendedor_ids = [ve.id_vendedor for ve in vendedores_empresas]

    # Query Usuario table to get vendor details with rol='vendedor'
    vendedores = Usuario.query.filter(Usuario.id.in_(vendedor_ids), Usuario.rol == 'vendedor').all()
    vendedores_info = [{
        "cedula": vendedor.cedula,
        "nombre": f"{vendedor.nombre} {vendedor.apellidos}",
        "telefono": vendedor.telefono,
        "email": vendedor.email
    } for vendedor in vendedores]

    return jsonify(vendedores_info)

@ruta_vendedor.route('/vendedor/info', methods=['GET'])
@token_required
def get_vendedor_info():
    vendedor_id = session.get('vendedor_id')
    if not vendedor_id:
        return jsonify({"error": "No vendor in session"}), 400

    vendedor = Usuario.query.get(vendedor_id)
    if not vendedor or vendedor.rol != 'vendedor':
        return jsonify({"error": "Vendor not found or incorrect role"}), 404

    vendedor_info = {
        "nombre": f"{vendedor.nombre} {vendedor.apellidos}",
        "rol": vendedor.rol
    }

    return jsonify(vendedor_info)

@ruta_vendedor.route('/add', methods=['POST'])
@token_required
def add_vendedor():
    data = request.json
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')
    telefono = data.get('telefono')
    email = data.get('email')
    cedula = data.get('cedula')
    usuario = data.get('usuario')
    contraseña = data.get('contraseña')
    direccion = data.get('direccion')
    rol = data.get('rol')
    empresa_id = session.get('empresa_id')

    if not all([nombre, apellidos, telefono, email, cedula, usuario, contraseña, direccion, rol]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        nuevo_vendedor = Usuario(
            nombre=nombre,
            apellidos=apellidos,
            telefono=telefono,
            email=email,
            cedula=cedula,
            usuario=usuario,
            contraseña=contraseña,
            direccion=direccion,
            rol=rol
        )
        db.session.add(nuevo_vendedor)
        db.session.commit()

        vendedor_empresa = VendedoresEmpresas(
            id_vendedor=nuevo_vendedor.id,
            id_empresa=empresa_id
        )
        db.session.add(vendedor_empresa)
        db.session.commit()

        return jsonify({"success": True}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
