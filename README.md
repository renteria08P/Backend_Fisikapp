# Backend Fisikapp

Backend desarrollado en **Django + Django REST Framework** para la gestión de laboratorios de física.

---

## Tecnologías utilizadas

- Python 
- Django 
- Django REST Framework
- JWT (SimpleJWT)
- Swagger (drf-yasg)
- CORS Headers
- Whitenoise

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