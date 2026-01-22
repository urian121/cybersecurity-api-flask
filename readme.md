# Flask JWT Auth API — Login Web + JSON, Dashboard Protegido

Proyecto mínimo de autenticación JWT con Flask y vista en Bootstrap 5. Incluye login (form y JSON), dashboard protegido por cookie JWT, manejo de 404 y logging a archivo.

## Stack
- Python 3.11+
- Flask 3.x, Flask-JWT-Extended 4.7.x, python-dotenv
- Bootstrap 5 (CDN)

## Configuración rápida
1. Crear entorno virtual (opcional):

```bash
python -m venv .venv && source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Variables de entorno en `.env` (ya incluido):

```env
JWT_SECRET_KEY=clave-secreta-muy-segura-2026
JWT_ACCESS_TOKEN_EXPIRES_HOURS=1
FLASK_DEBUG=true
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

## Ejecutar

```bash
python app.py
# o cambiar puerto al vuelo
FLASK_PORT=5050 python app.py
```

Abrir: `http://localhost:5000/` (o el puerto configurado).

## Credenciales de prueba
- Email: `dev@gmail.com`
- Password: `4825`

## Rutas
- GET `/` → Login (HTML)
- POST `/login` → JSON y Form. Ejemplo JSON:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"email":"dev@gmail.com","password":"4825"}' \
  http://localhost:5000/login
```

- GET `/dashboard` → Protegida; requiere cookie JWT (se setea tras login por formulario).
- GET `/logout` → Limpia cookie y redirige al login.

## Logging
- Archivo: `logs/app.log` (rotación 1MB, 3 backups)
- Registra: login exitoso, acceso a dashboard, 404 y access logs de Werkzeug.