from werkzeug.security import check_password_hash, generate_password_hash

def revisar_contraseña_hasheada(hash, contraseña):
    return check_password_hash(hash, contraseña)

def generar_contraseña_hasheada(contraseña):
    return generate_password_hash(contraseña)