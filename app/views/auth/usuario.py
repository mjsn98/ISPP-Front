# Importación de Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user

# Importación modular
from ...models.models import UsuarioDatos, Perfil, UsuarioPerfil,personal,alumno
from ...ext import db

# Desarrollo de la vista usuario
usuario = Blueprint('usuario', __name__)


@usuario.route('/')
@login_required
def index():
    # Obtener el perfil que es
    perfilid = 0
    session['usuarioperfilid']=UsuarioPerfil.get_usuarioperfilid(db,current_user.id, session['perfilid'])
    
    if session['perfilid'] != 7:
        session['personalid'] = personal.get_personalid(db,session['usuarioperfilid'])
    else:
        session['alumnoid'] = alumno.get_alumnoid_by_usuarioperfilid(db,session['usuarioperfilid'])

    if session['perfilid']:
        perfilid = session['perfilid']

    perfil = Perfil.get_perfil_via_id(db, perfilid)[0][1]
    consulta = UsuarioDatos.get_usuario_datos_id(db, current_user.id)
    return render_template('user/home.html', perfil=perfil, consulta=consulta)


# Se utiliza para obtener el nombre del perfil que selecciono actualmente
@usuario.route('/obtenernombredelperfil')
@login_required
def obtener_nombre_perfil():
    perfilid = 0
    if 'perfilid' in session:
        perfilid = session['perfilid']
    perfiles = Perfil.get_perfil_via_id(db, perfilid)[0][1]
    return jsonify({'Respuesta': perfiles})


@usuario.route('/obtenercountperfil')
@login_required
def obtener_count_perfiles():
    perfiles = UsuarioPerfil.get_count_usuarioperfil(db, current_user.id)[0]
    return jsonify({'Respuesta': perfiles})

@usuario.route('/DatosPersonales')
@login_required
def mostrar_Datospersonales_usuarioperfil():
    return render_template('user/perfiles/Datospersonales.html')