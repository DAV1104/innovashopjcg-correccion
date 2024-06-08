from flask import Flask, redirect, render_template, Blueprint

ruta_index = Blueprint('indexes_routes', __name__)

@ruta_index.route('/acceder', methods=['GET'])
def acceder_index():
    return render_template('index2.html')