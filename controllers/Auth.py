from flask import Blueprint, Flask, render_template, redirect, request, jsonify
from models.Administrador import Administrador, AdministradorSchema
from config.db import db, ma, app
from datetime import datetime, timedelta, timezone
import jwt
from .hashing_helper import verify_password

administrador_schema = AdministradorSchema()
administradores_schema = AdministradorSchema(many=True)

ruta_auth = Blueprint('auth_route', __name__)

SECRET_KEY = 'Bendiciones-para-todos'  # Ensure you have a secret key for JWT

def generar_token_admin(user_id):
    fecha_vencimiento = datetime.now(tz=timezone.utc) + timedelta(seconds=150)
    payload = {
        "exp": fecha_vencimiento,
        "user_id": user_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

@ruta_auth.route('/login', methods=['GET'])
def login():
    return render_template("admin-templates/login.html")

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

    token = generar_token_admin(administrador.id)
    response = jsonify({"success": True, "token": token})
    response.set_cookie('token', token)
    return response