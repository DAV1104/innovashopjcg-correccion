from flask import Blueprint, Flask, render_template, redirect, request, json, jsonify, session, make_response
from datetime import datetime, timedelta, timezone
import jwt
from config.db import db
from models.Usuario import Usuario, UsuarioSchema
from .hashing_helper import verify_password

ruta_vendedor = Blueprint('ruta_vendedor', __name__)
