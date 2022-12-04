# Importación de Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user

# Importación modular
from ....models.models import UsuarioDatos, Perfil
from ....ext import db

# Desarrollo de la vista docente
docente = Blueprint('docente', __name__)

@docente.route('/miscarreras')
@login_required
def mostrar_carreras_usuarioperfil():
    return render_template('user/perfiles/miscarreras.html')