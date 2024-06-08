from flask import Flask, render_template, request, jsonify, redirect, session, make_response
from config.db import app, db  # Assuming this sets up your Flask app

from controllers.Auth import ruta_auth
from controllers.Administrador import ruta_admin
from controllers.Usuarios import ruta_user
from controllers.Indexes import ruta_index  
from controllers.Empresa import ruta_empresa  # Import the new Empresa controller

# Register blueprints
app.register_blueprint(ruta_auth, url_prefix="/auth")
app.register_blueprint(ruta_admin, url_prefix="/admin")
app.register_blueprint(ruta_user, url_prefix="/user")
app.register_blueprint(ruta_empresa, url_prefix="/empresa")  # Register the new Empresa blueprint

app.register_blueprint(ruta_index, url_prefix="/")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
