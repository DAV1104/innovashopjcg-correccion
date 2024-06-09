from flask import Blueprint, request, jsonify, session, render_template
from models.Empresa import Empresa, EmpresaSchema
from models.Administrador import Administrador
from models.Modulos import Modulo
from models.Modulos_Empresas import ModuloEmpresa
from models.Usuario import Usuario
from config.db import db
from .hashing_helper import hash_password
from datetime import datetime

ruta_empresa = Blueprint('empresa_route', __name__)

empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)

DEFAULT_MODULES = ['clientes', 'vendedores', 'compras', 'cotizaciones', 'stock', 'informes']

@ruta_empresa.route('/home', methods=['GET'])
def show_home_enterprise():
    return render_template('empresas-templates/inicio_empresas.html')

@ruta_empresa.route('/clientes', methods=['GET'])
def list_clientes():
    usuarios = Usuario.query.all()
    return render_template('empresas-templates/empresas-clientes-list.html', usuarios=usuarios)

@ruta_empresa.route('/register', methods=['POST'])
def register_empresa():
    admin_id = session.get('user_id')
    admin = Administrador.query.get(admin_id)
    if not admin:
        return jsonify({"error": "Access denied"}), 403

    data = request.json
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

    existing_empresa = Empresa.query.filter(
        (Empresa.nombre == nombre) | 
        (Empresa.usuario == usuario) | 
        (Empresa.email == email) | 
        (Empresa.nit == nit)
    ).first()

    if existing_empresa:
        return jsonify({"error": "La empresa ya existe con el mismo nombre, usuario, email o NIT"}), 409

    session_limit_date = datetime.strptime(session_limit, '%Y-%m-%d') if session_limit else None

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

    db.session.add(new_empresa)
    db.session.commit()

    for module_name in DEFAULT_MODULES:
        modulo = Modulo.query.filter_by(nombre=module_name).first()
        if not modulo:
            modulo = Modulo(nombre=module_name, descripcion=module_name)
            db.session.add(modulo)
            db.session.commit()

        modulo_empresa = ModuloEmpresa(empresa_id=new_empresa.id, modulo_id=modulo.id)
        db.session.add(modulo_empresa)
    
    db.session.commit()

    return empresa_schema.jsonify(new_empresa)


@ruta_empresa.route('/<int:empresa_id>/modules', methods=['GET'])
def get_modules_for_company(empresa_id):
    empresa = Empresa.query.get(empresa_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    modules = db.session.query(Modulo.nombre, ModuloEmpresa.estado).join(ModuloEmpresa, Modulo.id == ModuloEmpresa.modulo_id).filter(ModuloEmpresa.empresa_id == empresa_id).all()
    module_status = {module.nombre: module.estado for module in modules}

    return jsonify({"modules": module_status})



@ruta_empresa.route('/update-module-status', methods=['POST'])
def update_module_status():
    data = request.json
    empresa_id = data.get('empresaId')
    modulo_nombre = data.get('moduloNombre')
    estado = data.get('estado')

    empresa = Empresa.query.get(empresa_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    modulo = Modulo.query.filter_by(nombre=modulo_nombre).first()
    if not modulo:
        return jsonify({"error": "Modulo no encontrado"}), 404

    modulo_empresa = ModuloEmpresa.query.filter_by(empresa_id=empresa.id, modulo_id=modulo.id).first()
    if not modulo_empresa:
        return jsonify({"error": "Relación Empresa-Modulo no encontrada"}), 404

    modulo_empresa.estado = estado
    db.session.commit()

    return jsonify({"success": "Estado del módulo actualizado correctamente"})

@ruta_empresa.route('/<int:empresa_id>/percentages', methods=['GET'])
def get_percentages_for_company(empresa_id):
    empresa = Empresa.query.get(empresa_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    return jsonify({
        "iva": empresa.tax,
        "ganancia": empresa.profit_percentage
    })

@ruta_empresa.route('/update-percentages', methods=['POST'])
def update_percentages():
    data = request.json
    empresa_id = data.get('empresaId')
    iva = data.get('iva')
    ganancia = data.get('ganancia')

    empresa = Empresa.query.get(empresa_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    empresa.tax = iva
    empresa.profit_percentage = ganancia
    db.session.commit()

    return jsonify({"success": "Percentages updated successfully"})


