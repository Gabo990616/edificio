Coloca aquí los archivos para que el proyecto funcione 100% OFFLINE.

Estructura esperada:
- vendor/bootstrap/css/bootstrap.min.css
- vendor/bootstrap/js/bootstrap.bundle.min.js
- vendor/bootstrap-icons/font/bootstrap-icons.min.css
- vendor/bootstrap-icons/font/fonts/  (carpeta con .woff2, etc)
- vendor/fontawesome/css/all.min.css
- vendor/fontawesome/webfonts/ (carpeta con fuentes)
- vendor/sweetalert2/sweetalert2.all.min.js  (o el build que uses)

Luego ejecuta: python manage.py collectstatic (si vas a servir estáticos desde staticfiles).
