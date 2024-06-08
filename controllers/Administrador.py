from flask import Blueprint, Flask, render_template, redirect, request, json, jsonify
from config.db import db, ma, app
from models.Administrador import Administrador

ruta_admin = Blueprint('admin_route', __name__)

@ruta_admin.route('/admin')
def homeadmin():
    return render_template('admin-templates/admin.html')

