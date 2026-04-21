import ssl
import random
import string
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string


# GENERAR PASSWORD AUTOMÁTICO
def generar_password(length=10):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(length))


# ENVIAR CORREO CON CREDENCIALES
def enviar_credenciales(user, password):

    # SOLO PARA LOCAL (evita error SSL)
    context = ssl._create_unverified_context()

    connection = get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        fail_silently=False
    )
    connection.ssl_context = context

    html_content = render_to_string('emails/credenciales_profesor.html', {
        'nombre': user.nombre,
        'correo': user.correo,
        'password': password,
    })

    email = EmailMultiAlternatives(
        subject='Acceso a FisikApp',
        body='Tu cuenta ha sido creada',
        from_email='FisikApp <fisikapp7@gmail.com>',
        to=[user.correo],
        connection=connection
    )

    email.attach_alternative(html_content, "text/html")
    email.send()