from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

# Reciclaje de codigo
'''
try:
    cur = mysql.connection.cursor()
    consulta = ("select * from y where x = %s")
    cur.execute(consulta, [(query)])
    return cur.fetchone()
except Exception as ex:
    print(ex)
    raise Exception(ex)
'''

class Usuario(UserMixin):
    def __init__(self, id=None, usuario=None, usuariocorreo=None, usuariocontraseña=None, usuariocontraseñatemp=False, usuarioestado=0):
        self.id = id
        self.usuario = usuario
        self.usuariocorreo = usuariocorreo
        self.usuariocontraseña = usuariocontraseña
        self.usuariocontraseñatemp = usuariocontraseñatemp
        self.usuarioestado = usuarioestado


    @classmethod
    def create_user(self, db, dni):
        try:
            cur = db.connection.cursor()
            consulta = ('INSERT INTO usuario(usuario,usuariocontraseñatemp) VALUES(%s,%s)')
            cur.execute(consulta, [dni,dni])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuario_DNI(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select * from usuario where usuario = %s")
            cur.execute(consulta, [(user.usuario)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuario_id(self, mysql, iduser):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select * from usuario where usuarioid = %s")
            cur.execute(consulta, [(iduser)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuario_email(self, mysql, user):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select * from usuario where usuariocorreo = %s")
            cur.execute(consulta, [(user.usuariocorreo)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuario_correo(self, mysql, correo):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select usuariocorreo from usuario where usuariocorreo = %s")
            cur.execute(consulta, [(correo)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def return_queried_user(self, mysql, user):
        try:
            row = Usuario.get_usuario_DNI(mysql, user)
            if row != None:
                temp = row[4]
                if row[5] == 0:
                    if str(temp) == str(user.usuariocontraseña):
                        temp = True
                        user = Usuario(row[0], row[1], row[2],
                                       row[3], temp, row[5])
                    else:
                        temp = False
                        user = Usuario(row[0], row[1], row[2],
                                       row[3], temp, row[5])
                    return user
                else:
                    if temp != None:
                        temp = True
                        user = Usuario(row[0], row[1], row[2],
                                       row[3], temp, row[5])
                    else:
                        temp = False
                        user = Usuario(row[0], row[1], row[2], Usuario.revisar_contraseña_hasheada(
                            row[3], user.usuariocontraseña), temp, row[5])
                    return user
            else:
                row = Usuario.get_usuario_email(mysql, user)
                if row != None:
                    user = Usuario(row[0], row[1], row[2], Usuario.revisar_contraseña_hasheada(
                        row[3], user.usuariocontraseña), row[4], row[5])
                    return user
                else:
                    return None
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_temp_password(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET UsuarioContraseñaTemp = NULL WHERE usuarioid = %s')
            cur.execute(consulta, [str(id)])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_temp_password_password(self, db, newpassword, correo):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET UsuarioContraseñaTemp = %s WHERE usuariocorreo = %s')
            cur.execute(consulta, [(newpassword), str(correo)])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_password(self, db, password, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET usuariocontraseña = %s WHERE usuarioid = %s')
            cur.execute(
                consulta, [Usuario.generar_contraseña_hasheada(password), id])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)
    
    @classmethod
    def resetear_contraseña(self, db, usuarioid):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET usuariocontraseñatemp = (select usuario from usuario where usuarioid = %s),usuariocontraseña = NULL, usuariocorreo = NULL, usuarioactivo = 0 WHERE usuarioid = %s')
            cur.execute(consulta, [usuarioid,usuarioid])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def update_email(self, db, email, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET usuariocorreo = %s WHERE usuarioid = %s')
            cur.execute(consulta, [email, id])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def activate_user(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET usuarioactivo = 1 WHERE usuarioid = %s')
            cur.execute(consulta, [(id)])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def deactivate_user(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuario SET usuarioactivo = 0 WHERE usuarioid = %s')
            cur.execute(consulta, [(id)])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def revisar_contraseña_hasheada(self, hash, contraseña):
        return check_password_hash(hash, contraseña)

    @classmethod
    def generar_contraseña_hasheada(self, contraseña):
        return generate_password_hash(contraseña)

    @classmethod
    def get_login_id(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = ("select * from usuario where usuarioid = %s")
            cur.execute(consulta, [(id)])
            row = cur.fetchone()
            if row != None:
                user = Usuario(row[0], row[1], row[2], row[3], row[4], row[5])
                return user
            else:
                return None

        except Exception as ex:
            print(ex)
            raise Exception(ex)


class Perfil():
    def __init__(self, id=None, perfil=None):
        self.id = id
        self.perfil = perfil

    @classmethod
    def get_all_perfiles(self, db):
        try:
            cur = db.connection.cursor()
            consulta = ("select * from perfil")
            cur.execute(consulta)
            return cur.fetchall()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_perfil_via_id(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = ("select * from perfil where perfilid = %s")
            cur.execute(consulta, [id])
            return cur.fetchall()
        except Exception as ex:
            print(ex)
            raise Exception(ex)


class UsuarioPerfil():
    def __init__(self, id=None, perfilid=None, usuarioid=None, usuarioperfilactivo=0):
        self.id = id
        self.perfilid = perfilid
        self.usuarioid = usuarioid
        self.usuarioperfilactivo = usuarioperfilactivo


    @classmethod
    def create_userperfil(self, db, usuarioid, perfilid):
        try:
            cur = db.connection.cursor()
            consulta = ('INSERT INTO usuarioperfil(perfilid, usuarioid) VALUES(%s,%s)')
            cur.execute(consulta, [int(perfilid),int(usuarioid)])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)



    @classmethod
    def get_usuarioperfilid(self, db, usuarioid, perfilid):
        try:
            cur = db.connection.cursor()
            consulta = ("select usuarioperfilid from usuarioperfil where usuarioid = %s and perfilid = %s")
            cur.execute(consulta, [usuarioid, perfilid])
            return cur.fetchone()[0]
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuarioperfil_via_user_activo(self, db, usuarioid, perfilid):
        try:
            cur = db.connection.cursor()
            consulta = ("select usuarioperfilactivo from usuarioperfil where usuarioid = %s and perfilid = %s")
            cur.execute(consulta, [usuarioid, perfilid])
            return cur.fetchone()[0]
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_perfilid_via_userid(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                "select perfilid from usuarioperfil where usuarioid = %s")
            cur.execute(consulta, [id])
            return cur.fetchall()
        except Exception as ex:
            print(ex)
            raise Exception(ex)
        

    @classmethod
    def get_count_usuarioperfil(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = ('select COUNT(UsuarioPerfilID) from usuarioperfil where usuarioid = %s')
            cur.execute(consulta, [id])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def activate_user_perfil(self, db, id, perfilid):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuarioperfil SET usuarioperfilactivo = 1 WHERE usuarioid = %s AND perfilid = %s')
            cur.execute(consulta, [id,perfilid])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def deactivate_user_perfil(self, db, id, perfilid):
        try:
            cur = db.connection.cursor()
            consulta = (
                'UPDATE usuarioperfil SET usuarioperfilactivo = 0 WHERE usuarioid = %s AND perfilid = %s')
            cur.execute(consulta, [id,perfilid])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_usuarioid_from_usuarioperfil(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                "select usuarioid from usuarioperfil where usuarioperfilid = %s")
            cur.execute(consulta, [id])
            usuarios = []
            usuarios.append(cur.fetchone()[0])
            usuarios.append(id)
            return usuarios
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    


class UsuarioDatos():
    def __init__(self, id=None, UsuarioNombre=None, UsuarioApellido=None, UsuarioCUIL=None, UsuarioFechaNac=None, UsuarioSexoDNI=None):
        self.id = id
        self.UsuarioNombre = UsuarioNombre
        self.UsuarioApellido = UsuarioApellido
        self.UsuarioCUIL = UsuarioCUIL
        self.UsuarioFechaNac = UsuarioFechaNac
        self.UsuarioSexoDNI = UsuarioSexoDNI
        
    @classmethod
    def get_usuario_datos_id(self, mysql, id):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select * from usuariodatos where usuarioid = %s")
            cur.execute(consulta, [(id)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)
        
    @classmethod
    def get_cuilfnac_id(self, mysql, id):
        try:
            cur = mysql.connection.cursor()
            consulta = ("select usuariocuil, usuariofechanac from usuariodatos where usuarioid = %s")
            cur.execute(consulta, [(id)])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

class Carpo():
    def __init__(self, carpoid, carreraid, plandeestudioid, orientacionid, carpoprograma, estado) -> None:
        self.carpoid = carpoid
        self.carreraid = carreraid
        self.plandeestudioid = plandeestudioid
        self.orientacionid = orientacionid
        self.carpoprograma = carpoprograma
        self.estado = estado

    @classmethod
    def get_carpo_nombres(self, mysql):
        try:
            cur = mysql.connection.cursor()
            consulta = ("SELECT carpoid, carreranombre, OrientacionID, plannombre FROM (carpo as c inner join carrera as car on c.CarreraID = car.carreraid) inner join plandeestudio as p on c.plandeestudioid = p.PlanID order by CARPOID")
            cur.execute(consulta)
            carpo = cur.fetchall()
            carpo2 = []
            for i in range(len(carpo)):
                
                if carpo[i][2] != None:
                    consulta = 'SELECT orientacionnombre FROM orientacion WHERE orientacionid = %s'
                    cur.execute(consulta,[carpo[i][2]])
                    list = [carpo[i][0],carpo[i][1],cur.fetchone()[0],carpo[i][3]]
                    carpo2.append(list)
                else:
                    carpo2.append(carpo[i])
            return carpo2
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_carpo_nombres_from_id(self, mysql,carpoid):
        try:
            cur = mysql.connection.cursor()
            consulta = ("SELECT carpoid, carreranombre, OrientacionID, plannombre FROM (carpo as c inner join carrera as car on c.CarreraID = car.carreraid) inner join plandeestudio as p on c.plandeestudioid = p.PlanID WHERE CARPOID = %s")
            cur.execute(consulta,[carpoid])
            carpo = cur.fetchall()
            carpo2 = []
            for i in range(len(carpo)):
                
                if carpo[i][2] != None:
                    consulta = 'SELECT orientacionnombre FROM orientacion WHERE orientacionid = %s'
                    cur.execute(consulta,[carpo[i][2]])
                    list = [carpo[i][0],carpo[i][1],cur.fetchone()[0],carpo[i][3]]
                    carpo2.append(list)
                else:
                    carpo2.append(carpo[i])

            return carpo2[0]
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_carpo_ids(self, mysql,carpoid):
        try:
            cur = mysql.connection.cursor()
            consulta = ("SELECT carreraid, orientacionid, plandeestudioid FROM carpo WHERE carpoid = %s")
            cur.execute(consulta,[carpoid])
            carpo = cur.fetchone()
            return carpo
        except Exception as ex:
            print(ex)
            raise Exception(ex)




class personalcarpo():
    def __init__(self, personalcarpoid, personalid, carpoid, personalcarpoactivo) -> None:
        
        self.personalcarpoid = personalcarpoid
        self.personalid = personalid
        self.carpoid = carpoid
        self.personalcarpoactivo = personalcarpoactivo

    @classmethod
    def cargar_personalcarpo(self,mysql, personalid, carpoid):
        try:
            cur = mysql.connection.cursor()
            consulta = ("INSERT INTO personalcarpo(personalid, carpoid) VALUES(%s,%s)")
            cur.execute(consulta,[personalid,carpoid])
            mysql.connection.commit()
            
            return True
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def eliminar_personalcarpo(self,mysql, personalid, carpoid):
        try:
            cur = mysql.connection.cursor()
            consulta = ("DELETE FROM personalcarpo WHERE CarpoID = %s and personalid = %s")
            cur.execute(consulta,[carpoid,personalid])
            mysql.connection.commit()
            
            return True
        except Exception as ex:
            print(ex)
            raise Exception(ex)
        

    @classmethod
    def cantcarpo(self,mysql, personalid):
        try:
            cur = mysql.connection.cursor()
            consulta = ("SELECT carpoid FROM personalcarpo where personalid = %s")
            cur.execute(consulta,[personalid])
            return cur.fetchall()
        except Exception as ex:
            print(ex)
            raise Exception(ex)


class personal():
    def __init__(self, personalid, usuarioperfilid) -> None:
        
        self.personalid = personalid
        self.usuarioperfilid = usuarioperfilid
    
    @classmethod
    def get_personalid(self, mysql, usuarioperfilid):
        try:
            cur = mysql.connection.cursor()
            consulta = ("SELECT personalid FROM personal WHERE usuarioperfilid = %s")
            cur.execute(consulta,[int(usuarioperfilid)])
            return cur.fetchone()[0]
        except Exception as ex:
            print(ex)
            raise Exception(ex)

class alumnocarpo():
    def __init__(self, alumnocarpoid, carpoid, alumnoid, alumnocarpoactivo) -> None:
        
        self.alumnocarpolid = alumnocarpoid
        self.carpoid = carpoid
        self.alumnoid = alumnoid
        self.alumnocarpoactivo = alumnocarpoactivo


    @classmethod
    def insert_alumnocarpo(self, db, alumnoid,carpoid):
        try:
            cur = db.connection.cursor()
            consulta = (
                'INSERT INTO alumnocarpo(alumnoid,carpoid) VALUES(%s,%s)')
            cur.execute(consulta, [alumnoid,carpoid])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    
    @classmethod
    def get_alumno_from_alumnocarpo(self, mysql, carpoid):
        try:
            cur = mysql.connection.cursor()
            consulta = ("SELECT alumnoid FROM alumnocarpo WHERE carpoid = %s")
            cur.execute(consulta,[int(carpoid)])
            alumnos = cur.fetchall()
            return alumnos
        except Exception as ex:
            print(ex)
            raise Exception(ex)
    
    @classmethod
    def get_carpoid_by_alumnoid(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                "select carpoid from alumnocarpo where alumnoid = %s")
            cur.execute(consulta, [id])
            return cur.fetchone()
        except Exception as ex:
            print(ex)
            raise Exception(ex)

class alumno():
    def __init__(self, alumnoid, usuarioperfilid) -> None:
        
        self.alumnolid = alumnoid
        self.usuarioperfilid = usuarioperfilid
    
    @classmethod
    def get_usuarioperfil_from_alumno(self, mysql, alumnoid):
        try:
            cur = mysql.connection.cursor()
            consulta = ('SELECT usuarioperfilid FROM alumno WHERE alumnoid = %s')
            cur.execute(consulta,[alumnoid])
            usuarioperfilesid=cur.fetchone()[0]
                # usuarioPerfilesid = cur.fetchall()
            return usuarioperfilesid
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def get_alumnoid_by_usuarioperfilid(self, db, id):
        try:
            cur = db.connection.cursor()
            consulta = (
                "select alumnoid from alumno where usuarioperfilid = %s")
            cur.execute(consulta, [id])
            return cur.fetchone()[0]
        except Exception as ex:
            print(ex)
            raise Exception(ex)

class usuarioDatos():
    def __init__(self, UsuarioID,UsuarioNombre,UsuarioApellido,UsuarioCUIL,UsuarioFechaNac,UsuarioSexoDNI) -> None:
        
        self.UsuarioID = UsuarioID
        self.UsuarioNombre = UsuarioNombre
        self.UsuarioApellido = UsuarioApellido
        self.UsuarioCUIL = UsuarioCUIL
        self.UsuarioFechaNac = UsuarioFechaNac
        self.UsuarioSexoDNI = UsuarioSexoDNI

    
    @classmethod
    def get_Nombre_Apellido_from_usuariodatos(self, mysql, usuarioid):
        try:
            cur = mysql.connection.cursor()
            consulta = ('SELECT UsuarioNombre,UsuarioApellido, observaciones FROM usuariodatos WHERE usuarioid = %s')
            cur.execute(consulta,[usuarioid])
            NombreApellido=cur.fetchone()
                # usuarioPerfilesid = cur.fetchall()
            return NombreApellido
        except Exception as ex:
            print(ex)
            raise Exception(ex)

    @classmethod
    def insert_usuariodatos(self, db,usuarioid, UsuarioNombre,UsuarioApellido, observaciones):
        try:
            cur = db.connection.cursor()
            consulta = ('INSERT INTO usuariodatos(usuarioid, UsuarioNombre,UsuarioApellido, observaciones) VALUES(%s,%s,%s,%s)')

            cur.execute(consulta, [usuarioid,UsuarioNombre,UsuarioApellido, observaciones])
            db.connection.commit()
            return cur.lastrowid
        except Exception as ex:
            print(ex)
            raise Exception(ex)