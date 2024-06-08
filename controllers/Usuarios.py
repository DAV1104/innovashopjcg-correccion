from flask import Blueprint, request, jsonify, redirect, session, make_response
from datetime import datetime, timedelta, timezone
import jwt
from config.db import db
from models.Usuario import Usuario, UsuarioSchema
from hashing_helper import verify_password

ruta_user = Blueprint('ruta_user', __name__)

SECRET_KEY = 'your_secret_key'  # Ensure you have a secret key for JWT

def generar_token(user_id, rol):
    fecha_vencimiento = datetime.now(tz=timezone.utc) + timedelta(seconds=150)
    payload = {
        "exp": fecha_vencimiento,
        "user_id": user_id,
        "rol": rol
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

@ruta_user.route('/login', methods=['POST'])
def login_user():
    data = request.json

    if not data["clave"] or not data["usuario"]:
        return jsonify({"error": "Uno o más campos están vacíos"}), 400

    usuario = Usuario.query.filter_by(usuario=data["usuario"]).first()

    if usuario is None or not verify_password(usuario.contraseña, data["clave"]):
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 404

    token = generar_token(usuario.id, usuario.rol)
    response = jsonify({"success": True, "token": token, "rol": usuario.rol})
    response.set_cookie('token', token)
    return response
