from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import current_user

# from ..models.models import Usuario

home = Blueprint("home", __name__)

@home.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('auth.verificar_roles'))
    return render_template("home.html")

@home.route("/testeo4")
def testeo4():
    return render_template("user/seleccionarperfil.html")