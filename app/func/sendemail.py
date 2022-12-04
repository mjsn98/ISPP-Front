from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()


class email:
    def __init__(self, emailreceptor, emailasunto, emailcuerpo) -> None:
        self.emailemisor = os.environ['MAIL_USERNAME']
        self.emailcontraseña = os.environ['MAIL_PASSWORD']
        self.emailreceptor = emailreceptor
        self.emailasunto = emailasunto
        self.emailcuerpo = emailcuerpo

    @classmethod
    def enviar_correo(self, email):
        try:
            em = EmailMessage()
            em['From'] = email.emailemisor
            em['To'] = email.emailreceptor
            em['Subject'] = email.emailasunto
            em.set_content(email.emailcuerpo)
            contexto = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as smtp:

                smtp.login(email.emailemisor, email.emailcontraseña)

                smtp.sendmail(email.emailemisor, email.emailreceptor, em.as_string().encode('utf-8'))
                
            return True
        except Exception as ex:
            print(ex)
            return False

    @classmethod
    def first_login(self, emailreceptor):
        emailasunto = 'Recuperar Contraseña'
        emailcuerpo = 'Correo registrado correctamente y contraseña actualizada'
        Email = email(emailreceptor, emailasunto, emailcuerpo)
        return email.enviar_correo(Email)

    @classmethod
    def solicitar_contraseña_temporal(self, emailreceptor, p):
        emailasunto = 'Recuperar Contraseña'
        emailcuerpo = f"Se solicito un cambio de contraseña\nSu contraseña temporal es {p}\nLa contraseña es de un solo uso, cambia la contraseña luego de iniciar"
        Email = email(emailreceptor, emailasunto, emailcuerpo)
        return email.enviar_correo(Email)
    
    @classmethod
    def notificar_cambio_contraseña(self, correo):
        asunto = 'Recuperar contraseña'
        cuerpo = 'Su contraseña ha sido cambiada exitosamente'
        Email = email(correo, asunto, cuerpo)
        return email.enviar_correo(Email)
            