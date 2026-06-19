# Backend Fisikapp

Backend desarrollado con Django REST Framework para la gestión integral de laboratorios de física, permitiendo la administración de usuarios, creación de laboratorios, inscripciones de estudiantes, seguimiento de actividades, generación de reportes y notificaciones dentro de la plataforma Fisikapp.

---

## Descripción

Fisikapp es una plataforma educativa diseñada para apoyar la enseñanza de la física mediante laboratorios interactivos y recursos digitales.

Este repositorio contiene la API REST encargada de:

Gestión de usuarios y roles.
Autenticación mediante JWT.
Administración de laboratorios.
Gestión de contenido educativo.
Inscripciones de estudiantes.
Sistema de notificaciones.
Generación de reportes PDF.
Integración con servicios externos para almacenamiento y envío de correos.

---

## Arquitectuta del Proyecto

Backend_Fisikapp/
│
├── Fisikapp/          # Configuración principal del proyecto
├── users/             # Usuarios, roles y autenticación
├── laboratorios/      # Gestión de laboratorios
├── contenido/         # Recursos y material educativo
├── inscripciones/     # Inscripciones de estudiantes
├── notificaciones/    # Sistema de notificaciones
├── parametros/        # Configuraciones generales
│
├── manage.py
├── requirements.txt

---

## Tecnologías principales

| Tecnología             | Uso                    |
| ---------------------- | ---------------------- |
| Django                 | Framework principal    |
| Django REST Framework  | API REST               |
| PostgreSQL             | Base de datos          |
| JWT                    | Autenticación          |
| Swagger                | Documentación          |
| Cloudinary             | Gestión de archivos    |
| SendGrid               | Correos electrónicos   |
| Pandas / OpenPyXL      | Procesamiento de Excel |
| ReportLab / WeasyPrint | Generación de PDF      |
| WhiteNoise             | Archivos estáticos     |
| Groq                   | Funcionalidades de IA  |

---

## Instalación del proyecto

1️⃣ Clonar el repositorio  
    git clone https://github.com/renteria08P/Backend_Fisikapp.git  
    cd Backend_Fisikapp  

2️⃣ Cambiar a la rama develop  
    git checkout develop  

3️⃣ Crear entorno virtual  
    python -m venv venv  

4️⃣ Activar entorno virtual (Windows)  
    venv\Scripts\activate  

5️⃣ Instalar dependencias  
    pip install --upgrade pip  
    pip install -r requirements.txt  

6️⃣ Aplicar migraciones  
    python manage.py migrate  

7️⃣ Ejecutar el servidor  
    python manage.py runserver  

---

## Variables de Entorno
El proyecto utiliza variables de entorno para proteger información sensible.

Algunas de las variables utilizadas son:

SECRET_KEY=

DEBUG=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

SENDGRID_API_KEY=

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

GROQ_API_KEY=

---

## Funcionalidades Principales

Usuarios
    - Registro de usuarios.
    - Inicio de sesión.
    - Recuperación de contraseña.
    - Gestión de roles y permisos.
Laboratorios
    - Creación y administración de laboratorios.
    - Gestión de recursos y contenido.
    - Seguimiento de actividades.
Inscripciones
    - Registro de estudiantes en laboratorios.
    - Control de acceso a prácticas.
Notificaciones
    - Notificaciones dentro de la plataforma.
    - Envío de correos electrónicos.
Reportes
    - Generación de documentos PDF.
    - Exportación de información.


---

## Despliegue

La aplicación se encuentra preparada para despliegues en plataformas compatibles con Django como:

Render
Railway

Utilizando:

Gunicorn
WhiteNoise
PostgreSQL


## ⚠️ Problemas comunes

Si aparece un error como: ModuleNotFoundError: No module named 'xxxx'

Ejecutar:

    pip install -r requirements.txt  

Si el problema persiste, instalar manualmente:

```bash
pip install django
pip install djangorestframework
pip install drf-yasg
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install whitenoise
python -m pip install Pillow
pip install python-dotenv
pip install cloudinary
pip install groq
pip install certifi
pip install sendgrid
pip install psycopg[binary]
pip install reportlab
pip install django-filter
pip install gunicorn whitenoise psycopg2-binary dj-database-url python-dotenv
pip install pandas openpyxl
pip install requests
pip install django-extensions
pip install qrcode[pil]

```

## Autor

Proyecto desarrollado como parte de una aplicación educativa orientada a la creación y gestión de laboratorios de física, enfocado en la simulación interactiva de fenómenos físicos y en el fortalecimiento del aprendizaje práctico mediante experiencias dinámicas, visuales e inmersivas, con el propósito de facilitar la comprensión de conceptos científicos y promover una enseñanza más didáctica e interactiva.