# Backend Fisikapp

Backend desarrollado en **Django + Django REST Framework** para la gestión de laboratorios de física, incluyendo autenticación, usuarios, notificaciones y envío de correos.

---

## Tecnologías utilizadas

- Python
- Django
- Django REST Framework
- JWT (SimpleJWT) – Autenticación
- Swagger (drf-yasg) – Documentación de API
- CORS Headers
- Whitenoise – Archivos estáticos
- SendGrid – Envío de correos

---

## Estructura del Proyecto

Backend_Fisikapp/
│── Fisikapp/          # Configuración principal
│── users/             # Gestión de usuarios
│── laboratorios/      # Lógica de laboratorios
│── inscripciones/     # Inscripción a prácticas
│── informes/          # Reportes
│── notificaciones/    # Sistema de notificaciones
│── contenido/         # Contenido educativo
│── parametros/        # Configuración dinámica
│── manage.py
│── requirements.txt
│── .env.example

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
Este proyecto utiliza variables de entorno para proteger información sensible.

❗ El archivo .env NO está incluido en el repositorio por seguridad.

Configuración
1. Crear un archivo .env en la raíz del proyecto
2. Copiar el contenido de .env.example
3. Reemplazar los valores con tus credenciales
    Ejemplo (.env.example)


## ⚠️ Problemas comunes

Si aparece un error como: ModuleNotFoundError: No module named 'xxxx'

Ejecutar:

    pip install -r requirements.txt  

Si el problema persiste, instalar manualmente:

pip install django  
pip install djangorestframework  
pip install drf-yasg  
pip install djangorestframework-simplejwt  
pip install django-cors-headers  
pip install whitenoise 
python -m pip install Pillow
pip install python-dotenv
pip install cloudinary



## Autor

Proyecto desarrollado como parte de una aplicación educativa para la creación y gestión de laboratorios de física con enfoque en simulación y aprendizaje interactivo.