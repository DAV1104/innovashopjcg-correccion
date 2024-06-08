from flask import Blueprint, Flask, render_template, redirect, request, json, jsonify, session
from datetime import datetime, timedelta, timezone
import jwt
from config.db import db
from models.Usuario import Usuario, UsuarioSchema
from .hashing_helper import verify_password

ruta_user = Blueprint('ruta_user', __name__)

@ruta_user.route('/login', methods=['GET'])
def login_route():
    return render_template('login.html')