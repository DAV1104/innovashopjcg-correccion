from flask import Flask, render_template, request, jsonify, redirect
from config.db import app, db
from models.Administrador import Administrador

from controllers.Auth import ruta_auth
from controllers.Administrador import ruta_admin

from controllers.hashing_helper import hash_password

# Register blueprints
app.register_blueprint(ruta_auth, url_prefix="/auth")
app.register_blueprint(ruta_admin, url_prefix="/")

@app.route('/', methods=['GET'])
def index():
    return redirect('/auth/login')

if __name__ == '__main__':
    app.run(debug=True)
