from flask import Blueprint, request, jsonify, session
from models.Empresa import Empresa, EmpresaSchema
from models.Administrador import Administrador
from config.db import db
from .hashing_helper import hash_password
from datetime import datetime

ruta_empresa = Blueprint('empresa_route', __name__)

empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)

@ruta_empresa.route('/register', methods=['POST'])
def register_empresa():
    # Check if the current user is an admin
    admin_id = session.get('user_id')
    admin = Administrador.query.get(admin_id)
    if not admin:
        return jsonify({"error": "Access denied"}), 403

    data = request.json

    # Extract data from the request
    nombre = data.get('nombre')
    direccion = data.get('direccion')
    telefono = data.get('telefono')
    email = data.get('email')
    usuario = data.get('usuario')
    nit = data.get('nit')
    contraseña = hash_password(data.get('contraseña'))
    session_limit = data.get('session_limit')
    general_discount = data.get('general_discount', 0.0)
    tax = data.get('tax', 0.0)
    profit_percentage = data.get('profit_percentage', 0.0)

    # Check for existing enterprise
    existing_empresa = Empresa.query.filter(
        (Empresa.nombre == nombre) | 
        (Empresa.usuario == usuario) | 
        (Empresa.email == email) | 
        (Empresa.nit == nit)
    ).first()

    if existing_empresa:
        return jsonify({"error": "La empresa ya existe con el mismo nombre, usuario, email o NIT"}), 409

    # Convert session_limit to datetime
    session_limit_date = datetime.strptime(session_limit, '%Y-%m-%d') if session_limit else None

    # Create new Empresa
    new_empresa = Empresa(
        nombre=nombre,
        direccion=direccion,
        telefono=telefono,
        email=email,
        usuario=usuario,
        contraseña=contraseña,
        nit=nit,
        session_limit=session_limit_date,
        general_discount=general_discount,
        tax=tax,
        profit_percentage=profit_percentage
    )

    # Add to database
    db.session.add(new_empresa)
    db.session.commit()

    return empresa_schema.jsonify(new_empresa)
