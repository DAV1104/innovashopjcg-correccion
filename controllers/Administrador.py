from flask import Blueprint, render_template, session, jsonify, request
from models.Administrador import Administrador
from models.Empresa import Empresa, EmpresaSchema
from config.db import app, db
from datetime import datetime

ruta_admin = Blueprint('admin_route', __name__)

empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)

@ruta_admin.route('/home')
def homeadmin():
    return render_template('admin-templates/admin.html')

@ruta_admin.route('/admin-percentages')
def show_percentages():
    return render_template('admin-templates/admin-percentages.html')

@ruta_admin.route('/admin-modulos')
def show_modules():
    query = request.args.get('query', '')
    if query:
        empresas = Empresa.query.filter(
            (Empresa.nombre.contains(query)) |
            (Empresa.nit.contains(query))
        ).all()
    else:
        empresas = Empresa.query.all()
    return render_template('admin-templates/admin-modulos.html', empresas=empresas)

@ruta_admin.route('/admin-empresas', methods=['GET'])
def show_enterprises():
    query = request.args.get('query', '')
    if query:
        empresas = Empresa.query.filter(
            (Empresa.nombre.contains(query)) |
            (Empresa.nit.contains(query))
        ).all()
    else:
        empresas = Empresa.query.all()
    return render_template('admin-templates/admin-empresas.html', empresas=empresas)

@ruta_admin.route('/search-empresas', methods=['GET'])
def search_enterprises():
    query = request.args.get('query', '')
    if query:
        empresas = Empresa.query.filter(
            (Empresa.nombre.contains(query)) |
            (Empresa.nit.contains(query))
        ).all()
    else:
        empresas = Empresa.query.all()
    return empresas_schema.jsonify(empresas)

@ruta_admin.route('/update-empresa-estado', methods=['POST'])
def update_empresa_estado():
    data = request.json
    nit = data.get('nit')
    nombre = data.get('nombre')
    estado = data.get('estado')

    empresa = Empresa.query.filter_by(nit=nit, nombre=nombre).first()
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    empresa.estado = estado
    db.session.commit()

    return jsonify({"success": True})


@ruta_admin.route('/admin-add-empresas', methods=['GET'])
def show_add_enterprises():
    return render_template('admin-templates/admin-add-empresas.html')

@ruta_admin.route('/login', methods=['GET'])
def login():
    return render_template("admin-templates/login.html")

@ruta_admin.route('/admin-info', methods=['GET'])
def admin_info():
    user_id = session.get('user_id')  # Assuming user_id is stored in the session
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    admin = Administrador.query.get(user_id)
    if not admin:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"nombre": admin.nombre})
