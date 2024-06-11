# main.py or app.py (your main application file)
from flask import Flask, render_template, request, jsonify, redirect, session, make_response
from config.db import app, db  # Assuming this sets up your Flask app

from controllers.Auth import ruta_auth
from controllers.Administrador import ruta_admin
from controllers.Usuarios import ruta_user
from controllers.Indexes import ruta_index  
from controllers.Empresa import ruta_empresa
from controllers.Cliente import ruta_cliente
from controllers.Proveedor import ruta_proveedor
from controllers.Producto import ruta_productos
from controllers.Vendedores import ruta_vendedor

# Register blueprints
app.register_blueprint(ruta_auth, url_prefix="/auth")
app.register_blueprint(ruta_admin, url_prefix="/admin")
app.register_blueprint(ruta_user, url_prefix="/user")
app.register_blueprint(ruta_empresa, url_prefix="/empresa")
app.register_blueprint(ruta_cliente, url_prefix="/cliente")
app.register_blueprint(ruta_proveedor, url_prefix="/proveedor")  # Ensure this line is correct
app.register_blueprint(ruta_productos, url_prefix="/producto")
app.register_blueprint(ruta_vendedor, url_prefix="/vendedor")

app.register_blueprint(ruta_index, url_prefix="/")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def unauthorized_error(e):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True)
