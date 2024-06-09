from flask import Blueprint, render_template, session, jsonify, request
from models.Administrador import Administrador
from models.Empresa import Empresa, EmpresaSchema
from .Auth import token_required
from config.db import app, db
from datetime import datetime

ruta_admin = Blueprint('admin_route', __name__)

empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)

@ruta_admin.route('/home')
@token_required
def homeadmin():
    if request.user_role != 'admin':
        return render_template('403.html'), 403
    return render_template('admin-templates/admin.html')

@ruta_admin.errorhandler(403)
@token_required
def unauthorized_error(e):
    return render_template('403.html'), 403

@ruta_admin.route('/admin-percentages')
@token_required
def show_percentages():
    return render_template('admin-templates/admin-percentages.html')

@ruta_admin.route('/admin-modulos')
@token_required
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

@ruta_admin.errorhandler(404)
def page_not_found_admin(e):
    return render_template('404.html'), 404

@ruta_admin.route('/admin-empresas', methods=['GET'])
@token_required
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
@token_required
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
@token_required
def show_add_enterprises():
    return render_template('admin-templates/admin-add-empresas.html')

@ruta_admin.route('/login', methods=['GET'])
@token_required
def login():
    return render_template("admin-templates/login.html")

@ruta_admin.route('/admin-info', methods=['GET'])
@token_required
def admin_info():
    user_id = session.get('user_id')  # Assuming user_id is stored in the session
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    admin = Administrador.query.get(user_id)
    if not admin:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"nombre": admin.nombre})
