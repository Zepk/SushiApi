# SushiApi

Si se necesitan modulos adicionales, anotarlos en requirements.txt

Siempre que se agregue algo a requirements.txt, hacer docker-compose build

Para montar el server, usar docker-compose up

Para bajarlo, docker-compose down

Las funciones que hace celery, estan definidas en tasks.py

Para ejecutar las funciones de celery se deben definir en settings.py en CELERY_BEAT_SCHEDULE

para hacer publico el servidor: cambiar     command: python manage.py runserver 0.0.0.0:8000 en docker-compose.yml a     command: python manage.py runserver 0.0.0.0:443 o     command: python manage.py runserver 0.0.0.0:80 (Creo)
