# Importación Modular
from ...ext import db
from ...models.models import Usuario
from ...models.models import UsuarioPerfil
from ...models.models import Perfil
from ...func.randomizer import generar_contraseña_temp
from ...func.sendemail import email

# Importación de Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user

# Desarrollo de la vista Login

auth = Blueprint('auth', __name__)

# Creación de la ruta login


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        # Obtener los Formularios del HTML
        usuario = request.form.get('Lcorreo')
        contrasenia = request.form.get('Lpassword')

        # Crear la Clase usuario
        user = Usuario(usuario=usuario,
                       usuariocontraseña=contrasenia, usuariocorreo=usuario)

        # Retorno del Usuario obtenido
        RetornoUsuario = Usuario.return_queried_user(db, user)

        # Preguntar si el usuario retornado no es nulo
        if RetornoUsuario != None:

            if RetornoUsuario.usuariocontraseña or RetornoUsuario.usuariocontraseñatemp:

                login_user(RetornoUsuario)  # Logear al Flask-Login

                # Si el usuario no esta activo, no tendrá contraseña ni correo
                if RetornoUsuario.usuarioestado == 0:
                    return redirect(url_for('auth.habilitar_usuario'))
                
                if RetornoUsuario.usuario != RetornoUsuario.usuariocontraseñatemp:
                    Usuario.update_temp_password(db, current_user.id)

                # Si el usuario posee una contraseña temporal, se realiza una redirección hacia cambiar contraseña
                if RetornoUsuario.usuariocontraseñatemp and not RetornoUsuario.usuariocontraseña:
                    return redirect(url_for('auth.cambiar_contraseña'))
                
                return redirect(url_for('auth.verificar_roles'))
            
            else:
                flash('Contraseña Incorrecta', category='error')
        else:
            flash('Usuario Inexistente', category='error')

    return render_template("user/login/log_in.html")


@auth.route('/verificacionderoles', methods=['GET'])
@login_required
def verificar_roles():
    # Si tiene mas de dos roles
    # Redirecciono al html "selecciona tu rol"
        
    id = current_user.id
    countperfiles = UsuarioPerfil.get_count_usuarioperfil(db, id)[0]
    if countperfiles >= 2:
        return redirect(url_for('auth.seleccionar_perfil'))
    else:
        # Si tiene un rol,
        # Redirecciona a su html correspondiente de su rol

        perfilobtenido = UsuarioPerfil.get_perfilid_via_userid(db, id)[0][0]

        # Se añade a la sesión actual, el perfil obtenido
        session['perfilid'] = perfilobtenido
        session['usuarioperfilactivo'] = UsuarioPerfil.get_usuarioperfil_via_user_activo(db, current_user.id, session['perfilid'])
        return redirect(url_for('usuario.index'))
        
    return jsonify({'Respuesta': 'No se pudo realizar la redirección'})


@auth.route('/seleccionarperfil', methods=['GET', 'POST'])
@login_required
def seleccionar_perfil():
    if request.method == 'GET':
        id = current_user.id
        perfiles = UsuarioPerfil.get_perfilid_via_userid(db, id)
        
        perfilesid = []
        perfilnames = []

        for i in perfiles:
            perfilesid.append(i[0])

        for i in perfilesid:
            perfilname = Perfil.get_perfil_via_id(db, i)[0]
            perfilnames.append(perfilname)

    if request.method == 'POST':
        perfilobtenido = int(request.form.get('opcion'))
    
        session['perfilid'] = perfilobtenido
        
        session['usuarioperfilactivo'] = UsuarioPerfil.get_usuarioperfil_via_user_activo(db, current_user.id, session['perfilid'])
                
        return redirect(url_for('usuario.index'))
    
        # if perfilobtenido == 1:
        #     return redirect(url_for('auth.adminview'))
        # elif perfilobtenido in [2, 3, 4, 6, 8]:
        #     return redirect(url_for('docente.index'))
        # elif perfilobtenido == 5:
        #     return redirect(url_for('bedel.index'))
        # elif perfilobtenido == 7:
        #     return redirect(url_for('alumno.index'))
        
    return render_template('user/seleccionarperfil.html', perfilnames=perfilnames)


@auth.route('/recuperarcontrasenia', methods=['GET', 'POST'])
def recuperar_contraseña():
    # genreacion y envio de contraseña temporal
    if request.method == 'POST':
        
        mail = request.form.get('correo')
        
        p = generar_contraseña_temp()

        correo = Usuario.get_usuario_correo(db, mail)[0]
        
        if correo:
            Email = email.solicitar_contraseña_temporal(mail, p)

            if Email:
                flash('Se ha enviado un correo con su nueva contraseña', category='success')
                Usuario.update_temp_password_password(db, p, mail)
                print(p)
                return redirect(url_for('auth.login'))
            else:
                flash('Error no se pudo enviar el email', category='error')
        else:
            flash('El correo solicitado no existe en la base de datos', category='error')

    return render_template('/user/login/recuperar_contraseña.html')


@auth.route('/cambiarcontraseña', methods=['POST', 'GET'])
def cambiar_contraseña():
    if request.method == 'GET':
        if current_user.is_authenticated:
            id = current_user.id
            logout_user()
        else:
            return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        id = request.form.get('id')
        contraseña1 = request.form.get('password')
        contraseña2 = request.form.get('passwordconfirm')

        if contraseña1 == contraseña2:
            
            Usuario.update_password(db, contraseña1, id)
            correo = Usuario.get_usuario_id(db, id)[2]
            email.notificar_cambio_contraseña(correo)

            # Inicio de sesión
            RetornoUsuario = Usuario.get_login_id(db, id)
            
            login_user(RetornoUsuario)
            
            flash('Contraseña establecidas correctamente!', category='sucess')

            return redirect(url_for('auth.verificar_roles'))
        else:
            flash('Las contraseñas no coinciden', category='error')
            return render_template('user/login/habilitar_usuario.html', id=id)

    return render_template('user/login/cambiar_contraseña.html', id=id)


@auth.route('/habilitarusuario', methods=['POST', 'GET'])
def habilitar_usuario():
    if request.method == 'GET':
        if current_user.is_authenticated:
            id = current_user.id
            logout_user()
            flash('Actualiza los siguientes datos para ingresar.')
        else:
            return redirect(url_for('auth.login'))

    if request.method == 'POST':
        id = request.form.get('id')
        correo = request.form.get('correo')
        contraseña1 = request.form.get('password')
        contraseña2 = request.form.get('passwordconfirm')

        if not (Usuario.get_usuario_correo(db, correo)):
            if contraseña1 == contraseña2:
                if email.first_login(correo):
                    Usuario.update_email(db, correo, id)
                    Usuario.update_password(db, contraseña1, id)
                    Usuario.update_temp_password(db, id)
                    Usuario.activate_user(db, id)

                    # Inicio de sesión
                    RetornoUsuario = Usuario.get_login_id(db, id)
                    login_user(RetornoUsuario)
                    
                    flash('¡Correo y Contraseña establecidas correctamente!', category='sucess')
                    return redirect(url_for('auth.verificar_roles'))
                else:
                    flash('Error al enviar el correo', category='error')
            else:
                flash('Las contraseñas no coinciden', category='error')
        else:
            flash('Ya existe un usuario con ese correo', category='warning')

    return render_template('user/login/habilitar_usuario.html', id=id)


# Creación de la ruta logout
@auth.route("/log-out")
@login_required
def logout():
    logout_user()
    if 'perfilid' in session:
        session.pop('perfilid', None)
    flash('El usuario ha cerrado la sesión correctamente')
    return redirect(url_for("home.index"))