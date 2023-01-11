# Web ISPP - FLASK
-A documentar-

## Instalación

*Opcional: crear un entorno virtual*

Instalar los requerimientos de Python:
`'pip install -r requirements.txt'`

Descargar el archivo 

> sql/DBISPPStructure.sql

Importar la base de datos en su RDBMS (Recomendado **MySQL**)

Se recomienda instalar y utilizar `python-dotenv`, para ejecutar los archivos .env - Editar las variables, sino según su sistema operativo establezca las variables en su SHELL

> FLASK_APP = entrypoint:app
> FLASK_ENV = development
> FLASK_DEBUG = true
> APP_SETTINGS_MODULE = config.default
> FLASK_RUN_HOST= 0.0.0.0
> FLASK_RUN_PORT= 8000
> MAIL_USERNAME='correo@gmail.com'
> MAIL_PASSWORD='password'

Es importante editar el MAIL_USERNAME y MAIL_PASSWORD para que se pueda enviar correos. A lo contrario de no hacerlo, pueden llegar errores y el malfuncionamiento del sistema

Se ejecuta el servidor con:

    flask run
