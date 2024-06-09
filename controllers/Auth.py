from flask import Blueprint, Flask, render_template, redirect, request, jsonify, session, url_for, abort
from models.Administrador import Administrador, AdministradorSchema
from models.Usuario import Usuario, UsuarioSchema
from models.Empresa import Empresa, EmpresaSchema
from config.db import db, ma, app
from datetime import datetime, timedelta, timezone
import jwt
from functools import wraps
from .hashing_helper import verify_password

administrador_schema = AdministradorSchema()
administradores_schema = AdministradorSchema(many=True)
user_schema = UsuarioSchema()
users_schema = UsuarioSchema(many=True)
empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)

ruta_auth = Blueprint('auth_route', __name__)

SECRET_KEY = 'Bendiciones-para-todos'

def generar_token(user_id, role):
    fecha_vencimiento = datetime.now(tz=timezone.utc) + timedelta(seconds=500)
    payload = {
        "exp": fecha_vencimiento,
        "user_id": user_id,
        "role": role
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token') or request.headers.get('Authorization')
        if not token:
            print("Token is missing!")
            return render_template('403.html', message="Token is missing!"), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = data['user_id']
            request.user_role = data['role']
            print(f"Token is valid. User ID: {request.user_id}, Role: {request.user_role}")
        except jwt.ExpiredSignatureError:
            print("Token has expired!")
            return render_template('403.html', message="Token has expired!"), 403
        except jwt.InvalidTokenError:
            print("Invalid token!")
            return render_template('403.html', message="Invalid token!"), 403

        return f(*args, **kwargs)
    return decorated



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

    token = generar_token(administrador.id, 'admin')
    response = jsonify({"success": True, "token": token})
    response.set_cookie('token', token, httponly=True)
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
        response.set_cookie('token', token, httponly=True)
        return response

    empresa = Empresa.query.filter_by(usuario=data["usuario"]).first()
    
    if empresa is not None and verify_password(empresa.contraseña, data["clave"]):
        if empresa.estado != 'activo':
            return jsonify({"error": "La empresa no está activa. Por favor, solicite más tiempo."}), 403
        
        # Store user information in session
        session['user_id'] = empresa.id
        session['nombre'] = empresa.nombre
        session['rol'] = empresa.rol

        token = generar_token(empresa.id, empresa.rol)
        response = jsonify({"success": True, "token": token, "rol": empresa.rol})
        response.set_cookie('token', token, httponly=True)
        return response

    return jsonify({"error": "Usuario o contraseña incorrectos"}), 404
@ruta_auth.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('admin_route.login'))
