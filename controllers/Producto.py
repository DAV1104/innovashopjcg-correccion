from flask import Flask, Blueprint, jsonify, request, session, url_for
from config.db import db, app
import os
from models.Producto import Producto
from models.Compra import Compra
from models.CompraDetalles import CompraDetalles
from models.ProductoAlterno import ProductoAlterno
from models.EmpresasDescuentosTime import EmpresasDescuentosTime
from werkzeug.utils import secure_filename
from models.Empresa import Empresa
from .Auth import token_required
from datetime import datetime, date

ruta_productos = Blueprint('ruta_productos', __name__)

# Define the path to the upload folder

# Allowed extensions for the upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ruta_productos.route('/add-stock', methods=['POST'])
@token_required
def add_stock():
    if 'img_src' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['img_src']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Ensure the upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(file_path)
            img_src = url_for('static', filename=f'img/{filename}', _external=False)
        except Exception as e:
            return jsonify({"error": "Failed to save file", "message": str(e)}), 500
        
        # Get other form data
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        existencias = request.form.get('existencias')
        min_existencias = request.form.get('min_existencias')
        categoria_id = request.form.get('categoria_id')
        proveedor_id = request.form.get('proveedor_id')
        producto_alterno_id = request.form.get('producto_alterno_id')
        
        # Convert precio and existencias to the correct types
        try:
            precio = float(precio)
            existencias = int(existencias)
        except ValueError:
            return jsonify({"error": "Invalid data type for precio or existencias"}), 400
        
        # Get IVA and ProfitPercentage from the Empresa table
        empresa = Empresa.query.filter_by(id=session['empresa_id']).first()
        if not empresa:
            return jsonify({"error": "Empresa not found"}), 404

        iva = empresa.tax
        profit_percentage = empresa.profit_percentage

        # Calculate precio_venta
        precio_venta = precio * (1 + iva / 100) * (1 + profit_percentage / 100)
        
        # Create a new product
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            precio_venta=precio_venta,
            existencias=existencias,
            min_existencias=min_existencias,
            img_src=img_src,
        )
        
        db.session.add(nuevo_producto)
        db.session.commit()
        
        # Create a new purchase
        nueva_compra = Compra(
            empresa_id=session['empresa_id'],
            proveedor_id=proveedor_id,
            fecha=datetime.utcnow()
        )
        db.session.add(nueva_compra)
        db.session.commit()
        
        # Create purchase details
        compra_detalles = CompraDetalles(
            compra_id=nueva_compra.id,
            producto_id=nuevo_producto.id,
            cantidad=existencias,
            precio_total=precio * existencias
        )
        db.session.add(compra_detalles)
        db.session.commit()
        
        # Create alternate product if provided
        if producto_alterno_id:
            producto_alterno = Producto.query.get(producto_alterno_id)
            if producto_alterno:
                producto_alterno = ProductoAlterno(
                    producto_id=nuevo_producto.id,
                    alterno_id=producto_alterno_id
                )
                db.session.add(producto_alterno)
                db.session.commit()
        
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Invalid file type"}), 400
    
@ruta_productos.route('/edit/<int:id>', methods=['PUT'])
@token_required
def edit_product(id):
    product = Producto.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.form
    product.nombre = data.get('nombre')
    product.descripcion = data.get('descripcion')
    product.precio = float(data.get('precio'))
    product.existencias = int(data.get('existencias'))
    product.min_existencias = int(data.get('min_existencias'))
    product.proveedor_id = int(data.get('proveedor_id'))
    product.producto_alterno_id = data.get('producto_alterno_id')

    if 'img_src' in request.files:
        file = request.files['img_src']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            product.img_src = url_for('static', filename=f'img/{filename}', _external=False)

    db.session.commit()
    return jsonify({"success": True})

@ruta_productos.route('/delete/<int:id>', methods=['DELETE'])
@token_required
def delete_product(id):
    product = Producto.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    try:
        # Find all CompraDetalles related to the product
        compra_detalles = CompraDetalles.query.filter_by(producto_id=id).all()
        compra_ids = [detalle.compra_id for detalle in compra_detalles]

        # Delete related entries in ProductoAlterno
        ProductoAlterno.query.filter((ProductoAlterno.producto_id == id) | (ProductoAlterno.alterno_id == id)).delete()

        # Delete related entries in CompraDetalles
        CompraDetalles.query.filter_by(producto_id=id).delete()

        # Delete related entries in Compra
        for compra_id in compra_ids:
            compra = Compra.query.get(compra_id)
            if compra:
                db.session.delete(compra)

        # Delete the product
        db.session.delete(product)
        db.session.commit()

        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete product", "message": str(e)}), 500
    
    
@ruta_productos.route('/all-products', methods=['GET'])
@token_required
def get_all_products():
    empresa_id = session['empresa_id']
    compras = Compra.query.filter_by(empresa_id=empresa_id).all()
    
    if not compras:
        return jsonify({"error": "No hay compras asociadas a esta empresa"}), 404

    compra_ids = [compra.id for compra in compras]
    compra_detalles = CompraDetalles.query.filter(CompraDetalles.compra_id.in_(compra_ids)).all()
    producto_ids = [detalle.producto_id for detalle in compra_detalles]

    productos = Producto.query.filter(Producto.id.in_(producto_ids)).all()

    productos_info = [{"id": producto.id, "nombre": producto.nombre} for producto in productos]

    return jsonify(productos_info)



@ruta_productos.route('/productos', methods=['GET'])
@token_required
def get_productos():

    empresa_id = session['empresa_id']
    query = request.args.get('query')

    compras = Compra.query.filter_by(empresa_id=empresa_id).all()

    if not compras:
        return jsonify({"error": "No hay compras asociadas a esta empresa"}), 404

    compra_ids = [compra.id for compra in compras]
    compra_detalles = CompraDetalles.query.filter(CompraDetalles.compra_id.in_(compra_ids)).all()
    producto_ids = [detalle.producto_id for detalle in compra_detalles]

    if query:
        productos = Producto.query.filter(Producto.id.in_(producto_ids), Producto.nombre.ilike(f'%{query}%')).all()
    else:
        productos = Producto.query.filter(Producto.id.in_(producto_ids)).all()
        
    empresa = Empresa.query.get(empresa_id)

    # Check for active discounts
    today = date.today()
    descuento = EmpresasDescuentosTime.query.filter(
        EmpresasDescuentosTime.empresa_id == empresa_id,
        EmpresasDescuentosTime.fecha_inicio <= today,
        EmpresasDescuentosTime.fecha_fin >= today
    ).first()

    productos_info = []
    for producto in productos:
        precio_venta = producto.precio * (1 + empresa.tax / 100) * (1 + empresa.profit_percentage / 100)
        if descuento:
            precio_venta *= (1 - descuento.porcentaje_descuento / 100)

        productos_info.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "precio_venta": round(precio_venta, 2),
            "img_src": producto.img_src,
            "iva": empresa.tax,
            "profit_percentage": empresa.profit_percentage,
            "descuento_activo": descuento.porcentaje_descuento if descuento else 0
        })

    return jsonify(productos_info)

@ruta_productos.route('/comprar', methods=['POST'])
@token_required
def comprar():
    data = request.json
    cart = data.get('cart')
    if not cart:
        return jsonify({"error": "Carrito vacío"}), 400

    empresa_id = session['user_id']
    proveedor_id = 1  # Placeholder value; you'll need to replace this with actual logic

    nueva_compra = Compra(
        empresa_id=empresa_id,
        proveedor_id=proveedor_id,
        fecha=datetime.utcnow()
    )
    db.session.add(nueva_compra)
    db.session.commit()

    for item in cart:
        detalle = CompraDetalles(
            compra_id=nueva_compra.id,
            producto_id=item['id'],
            cantidad=item['cantidad'],
            precio_total=item['precio'] * item['cantidad']
        )
        db.session.add(detalle)
    db.session.commit()

    return jsonify({"success": True})