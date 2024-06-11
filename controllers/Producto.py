from flask import Blueprint, jsonify, request, session
from config.db import db, app
import os
from models.Producto import Producto
from models.Compra import Compra
from models.CompraDetalles import CompraDetalles
from models.ProductoAlterno import ProductoAlterno
from werkzeug.utils import secure_filename
from models.Empresa import Empresa
from .Auth import token_required
from datetime import datetime

ruta_productos = Blueprint('ruta_productos', __name__)

UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        img_src = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Get other form data
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        existencias = request.form.get('existencias')
        min_existencias = request.form.get('min_existencias')
        categoria_id = request.form.get('categoria_id')
        proveedor_id = request.form.get('proveedor_id')
        producto_alterno_id = request.form.get('producto_alterno_id')
        
        # Create a new product
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            existencias=existencias,
            min_existencias=min_existencias,
            img_src=img_src,
            categoria_id=categoria_id
        )
        
        db.session.add(nuevo_producto)
        db.session.commit()
        
        # Create a new purchase
        nueva_compra = Compra(
            empresa_id=session['user_id'],
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

@ruta_productos.route('/productos', methods=['GET'])
@token_required
def get_productos():
    empresa_id = session['user_id']
    compras = Compra.query.filter_by(empresa_id=empresa_id).all()

    if not compras:
        return jsonify({"error": "No hay compras asociadas a esta empresa"}), 404

    compra_ids = [compra.id for compra in compras]
    compra_detalles = CompraDetalles.query.filter(CompraDetalles.compra_id.in_(compra_ids)).all()
    producto_ids = [detalle.producto_id for detalle in compra_detalles]

    productos = Producto.query.filter(Producto.id.in_(producto_ids)).all()
    empresa = Empresa.query.get(empresa_id)
    productos_info = [{
        "id": producto.id,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio": producto.precio,
        "img_src": producto.img_src,
        "iva": empresa.tax,
        "profit_percentage": empresa.profit_percentage
    } for producto in productos]

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