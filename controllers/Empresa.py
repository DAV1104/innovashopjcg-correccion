from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from models.Empresa import Empresa, EmpresaSchema
from models.Administrador import Administrador
from models.Modulos import Modulo
from models.Modulos_Empresas import ModuloEmpresa
from models.ClientesEmpresas import ClientesEmpresas
from models.Usuario import Usuario
from models.EmpresasDescuentosTime import EmpresasDescuentosTime
from .Auth import token_required, admin_required, empresa_required
from config.db import db
from .hashing_helper import hash_password
from datetime import datetime, timedelta

ruta_empresa = Blueprint('empresa_route', __name__)

empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)

DEFAULT_MODULES = ['clientes', 'vendedores', 'compras', 'cotizaciones', 'proveedores']

@ruta_empresa.route('/empresa-info', methods=['GET'])
@token_required
@empresa_required
def empresa_info():
    user_id = session.get('empresa_id')
    empresa = Empresa.query.get(user_id)
    return jsonify({
        "nombre": empresa.nombre.capitalize(),
        "rol": empresa.rol.capitalize(),
        "estado": empresa.estado
    })
    
@ruta_empresa.route('/descuentos', methods=['POST'])
@token_required
def aplicar_descuento():
    data = request.json
    porcentaje_descuento = data.get('porcentaje_descuento')
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')
    empresa_id = session['empresa_id']

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        nuevo_descuento = EmpresasDescuentosTime(
            porcentaje_descuento=porcentaje_descuento,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            empresa_id=empresa_id
        )
        db.session.add(nuevo_descuento)
        db.session.commit()
        return jsonify({"success": True}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@ruta_empresa.route('/descuentos', methods=['GET'])
@token_required 
@empresa_required
def aplicar_descuentos():
    return render_template('empresas-templates/descuentos-empresas.html')

@ruta_empresa.route('/home', methods=['GET'])
@token_required
@empresa_required
def show_home_enterprise():
    return render_template('empresas-templates/inicio_empresas.html')

@ruta_empresa.route('/proveedores', methods=['GET'])
@token_required
@empresa_required
def show_proveedores():
    return render_template('empresas-templates/proveedores-empresas.html')

@ruta_empresa.route('stock')
@token_required
@empresa_required
def show_stock():
    return render_template('empresas-templates/stock-empresas.html')

@ruta_empresa.route('/add-proveedor', methods=['GET'])
@token_required
@empresa_required
def add_proveedor_form():
    return render_template('empresas-templates/add-proveedores-empresas.html')

@ruta_empresa.route('/vendedores-list')
@token_required
@empresa_required
def show_vendedores():
    return render_template('empresas-templates/vendedores2-empresas.html')

@ruta_empresa.route('/modificar-sesion', methods=['POST'])
@token_required
@admin_required
def modificar_sesion():
    data = request.json
    empresa_id = data.get('empresaId')
    meses = data.get('meses')
    accion = data.get('accion')  # This will be either 'extender' or 'disminuir'

    if not empresa_id or not meses or not accion:
        return jsonify({"error": "Datos incompletos"}), 400

    empresa = Empresa.query.get(empresa_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    try:
        if accion == 'extender':
            empresa.session_limit = empresa.session_limit + timedelta(days=int(meses) * 30)
        elif accion == 'disminuir':
            empresa.session_limit = empresa.session_limit - timedelta(days=int(meses) * 30)

        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ruta_empresa.route('/eliminar-empresa/<int:empresa_id>', methods=['DELETE'])
@token_required
@admin_required
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
@empresa_required
def list_clientes():
    empresa_id = session.get('empresa_id') 
    if not empresa_id:
        return jsonify({"error": "Not logged in"}), 401

    cliente_ids = db.session.query(ClientesEmpresas.usuario_id).filter_by(empresa_id=empresa_id).all()
    cliente_ids = [id[0] for id in cliente_ids]

    usuarios = Usuario.query.filter(Usuario.id.in_(cliente_ids), Usuario.rol == "cliente").all()

    return render_template('empresas-templates/empresas-clientes-list.html', usuarios=usuarios)

@ruta_empresa.route('/api/clientes', methods=['GET'])
@token_required
@empresa_required
def api_list_clientes():
    empresa_id = session.get('empresa_id')
    if not empresa_id:
        return jsonify({"error": "Not logged in"}), 401

    query = request.args.get('query', '')
    
    cliente_ids = db.session.query(ClientesEmpresas.usuario_id).filter_by(empresa_id=empresa_id).all()
    cliente_ids = [id[0] for id in cliente_ids] 

    if query:
        usuarios = Usuario.query.filter(
            Usuario.id.in_(cliente_ids),
            Usuario.rol == "cliente",
            (Usuario.nombre.contains(query) | Usuario.apellidos.contains(query) | Usuario.cedula.contains(query))
        ).all()
    else:
        usuarios = Usuario.query.filter(Usuario.id.in_(cliente_ids), Usuario.rol == "cliente").all()

    usuarios_data = [{"id": usuario.id, "cedula": usuario.cedula, "nombre": usuario.nombre, "apellidos": usuario.apellidos, "telefono": usuario.telefono, "email": usuario.email} for usuario in usuarios]
    
    return jsonify(usuarios_data)

@ruta_empresa.route('/register', methods=['POST'])
@token_required
@admin_required
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

    # If no modules are found, create the default modules and associate them with the empresa
    if not modules:
        default_active_modules = ['clientes', 'vendedores', 'compras', 'cotizaciones']
        for module_name in DEFAULT_MODULES:
            modulo = Modulo.query.filter_by(nombre=module_name).first()
            if not modulo:
                modulo = Modulo(nombre=module_name, descripcion=module_name)
                db.session.add(modulo)
                db.session.commit()
            
            estado = module_name in default_active_modules
            modulo_empresa = ModuloEmpresa(empresa_id=empresa.id, modulo_id=modulo.id, estado=estado)
            db.session.add(modulo_empresa)
        db.session.commit()

        # Fetch the modules again after creating them
        modules = db.session.query(Modulo.nombre, ModuloEmpresa.estado).join(ModuloEmpresa, Modulo.id == ModuloEmpresa.modulo_id).filter(ModuloEmpresa.empresa_id == empresa_id).all()

    module_status = {module.nombre: module.estado for module in modules}

    return jsonify({"modules": module_status})

@ruta_empresa.route('/update-module-status', methods=['POST'])
@admin_required
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
@admin_required
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
@admin_required
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
