from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from models.Empresa import Empresa, EmpresaSchema
from models.Administrador import Administrador
from models.Modulos import Modulo
from models.Modulos_Empresas import ModuloEmpresa
from models.ClientesEmpresas import ClientesEmpresas
from models.Usuario import Usuario
from .Auth import token_required 
from config.db import db
from .hashing_helper import hash_password
from datetime import datetime, timedelta

ruta_empresa = Blueprint('empresa_route', __name__)

empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)

DEFAULT_MODULES = ['clientes', 'vendedores', 'compras', 'cotizaciones', 'stock', 'informes']

from flask import Blueprint, request, jsonify, session, redirect, url_for
from models.Empresa import Empresa
from models.Usuario import Usuario

ruta_empresa = Blueprint('empresa_route', __name__)

@ruta_empresa.route('/add-clientes', methods=['GET', 'POST'])
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

@ruta_empresa.route('/empresa-info', methods=['GET'])
@token_required
def empresa_info():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    empresa = Empresa.query.get(user_id)
    if not empresa:
        return jsonify({"error": "Empresa not found"}), 404

    if empresa.estado != 'activo':
        return jsonify({"error": "Esta empresa no se encuentra activa"}), 403

    return jsonify({
        "nombre": empresa.nombre.capitalize(),
        "rol": empresa.rol.capitalize(),
        "estado": empresa.estado
    })

@ruta_empresa.route('/home', methods=['GET'])
@token_required
def show_home_enterprise():
    return render_template('empresas-templates/inicio_empresas.html')

@ruta_empresa.route('/extender-sesion', methods=['POST'])
def extender_sesion():
    data = request.json
    empresa_id = data.get('empresaId')
    meses = data.get('meses')

    if not empresa_id or not meses:
        return jsonify({"error": "Datos incompletos"}), 400

    empresa = Empresa.query.get(empresa_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    try:
        empresa.session_limit = empresa.session_limit + timedelta(days=int(meses) * 30)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ruta_empresa.route('/eliminar-empresa/<int:empresa_id>', methods=['DELETE'])
@token_required
def eliminar_empresa(empresa_id):
    empresa = Empresa.query.get(empresa_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    try:
        # First delete related rows in modulosempresas
        ModuloEmpresa.query.filter_by(empresa_id=empresa_id).delete()
        db.session.commit()

        # Then delete the empresa
        db.session.delete(empresa)
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500

@ruta_empresa.route('/clientes', methods=['GET'])
@token_required
def list_clientes():
    usuarios = Usuario.query.all()
    return render_template('empresas-templates/empresas-clientes-list.html', usuarios=usuarios)

@ruta_empresa.route('/register', methods=['POST'])
@token_required
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

    # List of default modules to be set as active
    default_active_modules = ['clientes', 'vendedores', 'compras', 'cotizaciones']

    for module_name in DEFAULT_MODULES:
        modulo = Modulo.query.filter_by(nombre=module_name).first()
        if not modulo:
            modulo = Modulo(nombre=module_name, descripcion=module_name)
            db.session.add(modulo)
            db.session.commit()

        estado = module_name in default_active_modules
        modulo_empresa = ModuloEmpresa(empresa_id=new_empresa.id, modulo_id=modulo.id, estado=estado)
        db.session.add(modulo_empresa)
    
    db.session.commit()

    return empresa_schema.jsonify(new_empresa)



@ruta_empresa.route('/<int:empresa_id>/modules', methods=['GET'])
@token_required
def get_modules_for_company(empresa_id):
    empresa = Empresa.query.get(empresa_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    modules = db.session.query(Modulo.nombre, ModuloEmpresa.estado).join(ModuloEmpresa, Modulo.id == ModuloEmpresa.modulo_id).filter(ModuloEmpresa.empresa_id == empresa_id).all()
    module_status = {module.nombre: module.estado for module in modules}

    return jsonify({"modules": module_status})



@ruta_empresa.route('/update-module-status', methods=['POST'])
@token_required
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
@token_required
def get_percentages_for_company(empresa_id):
    empresa = Empresa.query.get(empresa_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    return jsonify({
        "iva": empresa.tax,
        "ganancia": empresa.profit_percentage
    })

@ruta_empresa.route('/update-percentages', methods=['POST'])
@token_required
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
