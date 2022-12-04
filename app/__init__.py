from flask import Flask, jsonify, redirect, url_for

from .ext import db, LogMan

from .models.models import Usuario

def create_app(Settings_Module):
    #crear la app de fabrica
    app = Flask(__name__)
    #Configuración del objeto 
    app.config.from_object(Settings_Module)
       
    #inicialización de modulos externos
    db.init_app(app)
    LogMan.init_app(app)
        
    # Registración de Blueprints
    from .views.home import home
    from .views.auth.auth import auth
    from .views.auth.user.alumno import alumno
    from .views.auth.user.bedel import bedel
    from .views.auth.user.docente import docente
    from .views.auth.usuario import usuario
    
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(usuario, url_prefix="/user")
    
    app.register_blueprint(bedel, url_prefix="/user/bedel")
    app.register_blueprint(docente, url_prefix="/user/docente")
    app.register_blueprint(alumno, url_prefix="/user/alumno")
    
    
    # Logeo
    @LogMan.user_loader
    def user_loader(id):
        return Usuario.get_login_id(db, id)
    
    LogMan.login_view = "auth.login" #vista del login
    LogMan.login_message = "Inicie la sesión para acceder a esta pagina"
    LogMan.login_message_category = "warning"
    
    
    # Registro de error handlers
    @app.errorhandler(400)
    def handler400Error(error):
        return jsonify({'error': 'Bad Request'}), 400

    @app.errorhandler(401)
    def handler401Error(error):
        return redirect(url_for('index'))

    @app.errorhandler(404)
    def handler404Error(error):
        return jsonify({'error': 'NotFound'}), 404

    @app.errorhandler(500)
    def handler500error(error):
        return jsonify({'error': 'Error a la hora de conectar a la base de datos'}), 500

    app.register_error_handler(400, handler400Error)
    app.register_error_handler(401, handler401Error)
    app.register_error_handler(404, handler404Error)
    app.register_error_handler(500, handler500error)
    
    return app