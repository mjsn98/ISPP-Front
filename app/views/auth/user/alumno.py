# Importación de Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user

# Importación modular
from ....models.models import UsuarioDatos, Perfil,Carpo,alumnocarpo
from ....ext import db

# Desarrollo de la vista Alumno
alumno = Blueprint('alumno', __name__)

@alumno.route('/miscarreras')
@login_required
def mostrar_carreras_usuarioperfil():

    carpoTotales = Carpo.get_carpo_nombres(db)
    if session['usuarioperfilactivo'] == 0:
        
        return render_template('user/perfiles/Alumnos/añadircarpo.html', carpo = carpoTotales)
    else:
        print(alumnocarpo.get_carpoid_by_alumnoid(db,session['alumnoid']))
        # carpoid = personalcarpo.cantcarpo(db,session['alumnolid'])
        # carposUsuario=[]
        # for i in carpoid:
        #     carpo = Carpo.get_carpo_nombres_from_id(db,i)
        #     carposUsuario.append(carpo)
        # aux = []
        # for car in carpoTotales:
        #     for i in carpoid:
        #         if(car[0] == i[0]):
        #             aux.append(car)
                    
        # for a in aux:
        #     carpoTotales.remove(a)

        
        return render_template('user/perfiles/Alumnos/miscarreras.html', carpo = carpoTotales)

@alumno.route('/datossecundaria')
@login_required
def mostrar_datossecundaria_usuarioperfil():

    return render_template('user/perfiles/Alumnos/datossecundaria.html')

@alumno.route('/datosacademicos')
@login_required
def mostrar_datosacademicos_usuarioperfil():

    return render_template('user/perfiles/Alumnos/datosacademicos.html')

@alumno.route('/activaralumno', methods = ['POST'])
@login_required
def activar_alumno():
    # carpoid = request.form.get('Carpo')

    # if personalcarpo.cargar_personalcarpo(db,session['personalid'], carpoid):
    #     UsuarioPerfil.activate_user_perfil(db, current_user.id, session['perfilid'])
    #     session['usuarioperfilactivo'] = 1

    return redirect(url_for('bedel.mostrar_carreras_usuarioperfil'))