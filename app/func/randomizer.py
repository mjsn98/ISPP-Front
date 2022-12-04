from random import choice

def generar_contraseña_temp():    
    longitud = 10
    valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ=@#%&+"
    p=''
    p = p.join([choice(valores) for i in range(longitud)])
    return p