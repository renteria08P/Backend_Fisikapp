import ssl
import random
import string
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from sendgrid.helpers.mail import Mail
import os
from sendgrid import SendGridAPIClient

# GENERAR PASSWORD AUTOMÁTICO
def generar_password(length=10):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(length))


# ENVIAR CORREO CON CREDENCIALES
def enviar_credenciales(user, password):
    html_content = render_to_string('emails/credenciales_profesor.html', {
        'nombre': user.nombre,
        'correo': user.correo,
        'password': password,
    })

    message = Mail(
        from_email='fisikapp7@gmail.com',
        to_emails=user.correo,
        subject='Acceso a FisikApp',
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print("Correo enviado:", response.status_code)
    except Exception as e:
        print("Error al enviar correo:", str(e))