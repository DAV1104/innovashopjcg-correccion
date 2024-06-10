from flask import Blueprint, Flask, render_template, redirect, request, json, jsonify, session
from datetime import datetime, timedelta, timezone
import jwt
from config.db import db
from models.Usuario import Usuario, UsuarioSchema
from models.ClientesEmpresas import ClientesEmpresas
from .Auth import token_required
from .hashing_helper import verify_password, hash_password

ruta_cliente = Blueprint('ruta_cliente', __name__)

@ruta_cliente.route('/home', methods=['GET'])
def login_route():
    return render_template('cliente.html')

@ruta_cliente.route('/add-clientes', methods=['GET', 'POST'])
@token_required
def add_clientes():
    if request.method == 'GET':
        return render_template('empresas-templates/clientes-empresas.html')
    
    if request.method == 'POST':
        data = request.json
        nombre = data.get('nombre')
        apellidos = data.get('apellidos')
        nit = data.get('nit')
        direccion = data.get('direccion')
        telefono = data.get('telefono')
        email = data.get('email')
        contraseña = hash_password(data.get('contraseña'))

        # Create new client user
        nuevo_cliente = Usuario(
            nombre=nombre,
            apellidos=apellidos,
            usuario=email,
            contraseña=contraseña,
            rol='cliente',
            cedula=nit,
            direccion=direccion,
            telefono=telefono,
            email=email
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()

        # Relate new client with the current company
        empresa_id = session.get('user_id')
        nuevo_cliente_empresa = ClientesEmpresas(
            usuario_id=nuevo_cliente.id,
            empresa_id=empresa_id
        )

        db.session.add(nuevo_cliente_empresa)
        db.session.commit()

        return jsonify({"success": True})