from flask import Blueprint, Flask, render_template, redirect, request, jsonify, session, url_for
from models.Administrador import Administrador, AdministradorSchema
from models.Usuario import Usuario, UsuarioSchema
from models.Empresa import Empresa, EmpresaSchema
from config.db import db, ma, app
from datetime import datetime, timedelta, timezone
import jwt
from .hashing_helper import verify_password

administrador_schema = AdministradorSchema()
administradores_schema = AdministradorSchema(many=True)
user_schema = UsuarioSchema()
users_schema = UsuarioSchema(many=True)
empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)

ruta_auth = Blueprint('auth_route', __name__)

SECRET_KEY = 'Bendiciones-para-todos'

def generar_token(user_id):
    fecha_vencimiento = datetime.now(tz=timezone.utc) + timedelta(seconds=150)
    payload = {
        "exp": fecha_vencimiento,
        "user_id": user_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

@ruta_auth.route('/ingreso-admin', methods=['POST'])
def login_admin():
    data = request.json

    if not data["clave"] or not data["usuario"]:
        return jsonify({"error": "Uno o más campos están vacíos"}), 400

    administrador = Administrador.query.filter_by(
        usuario=data["usuario"],
    ).first()

    if administrador is None or not verify_password(administrador.contraseña, data["clave"]):
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 404

    # Store user information in session
    session['user_id'] = administrador.id
    session['nombre'] = administrador.nombre

    token = generar_token(administrador.id)
    response = jsonify({"success": True, "token": token})
    response.set_cookie('token', token)
    return response

@ruta_auth.route('/login', methods=['POST'])
def login_user():
    data = request.json

    if not data["clave"] or not data["usuario"]:
        return jsonify({"error": "Uno o más campos están vacíos"}), 400

    usuario = Usuario.query.filter_by(usuario=data["usuario"]).first()
    
    if usuario is not None and verify_password(usuario.contraseña, data["clave"]):
        # Store user information in session
        session['user_id'] = usuario.id
        session['nombre'] = usuario.nombre
        session['rol'] = usuario.rol

        token = generar_token(usuario.id, usuario.rol)
        response = jsonify({"success": True, "token": token, "rol": usuario.rol})
        response.set_cookie('token', token)
        return response

    empresa = Empresa.query.filter_by(usuario=data["usuario"]).first()
    
    if empresa is not None and verify_password(empresa.contraseña, data["clave"]):
        # Store user information in session
        session['user_id'] = empresa.id
        session['nombre'] = empresa.nombre
        session['rol'] = empresa.rol

        token = generar_token(empresa.id, empresa.rol)
        response = jsonify({"success": True, "token": token, "rol": empresa.rol})
        response.set_cookie('token', token)
        return response

    return jsonify({"error": "Usuario o contraseña incorrectos"}), 404

@ruta_auth.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('admin_route.login'))
