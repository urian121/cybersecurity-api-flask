from flask import Flask, jsonify, request, render_template, redirect, url_for
from services.logger import configure_logging
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
)
import datetime # Para manejar fechas y horas
import os 
from dotenv import load_dotenv # Para cargar variables de entorno desde un archivo .env

load_dotenv() # Carga las variables de entorno desde el archivo .env

# Inicialización de la aplicación Flask
app = Flask(__name__)

# En producción, usa variables de entorno para la Secret Key
secret_key = os.getenv("JWT_SECRET_KEY")
if not secret_key:
    raise RuntimeError("JWT_SECRET_KEY no configurada")

app.config["JWT_SECRET_KEY"] = secret_key
expires_hours = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "1"))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=expires_hours)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_SECURE"] = False


jwt = JWTManager(app) # Inicializa el manejador de tokens JWT para la aplicación Flask
configure_logging(app)

# Base de datos simulada
users_db = {
    "usuario":"dev@gmail.com", "password":"4825"
}


def responder(msg, status):
    """Simplifica la respuesta según si es API o Navegador"""
    if request.is_json:
        return jsonify({"msg": msg}), status
    return render_template("index.html", error=msg), status

@app.route("/login", methods=["POST"])
def login():
    # 1. Obtener datos de cualquier fuente (JSON o Formulario)
    data = request.get_json(silent=True) or request.form
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    # 2. Validaciones rápidas (Guard Clauses)
    if not email or not password:
        return responder("Email y contraseña requeridos", 400)
    
    if email != users_db.get("usuario"):
        return responder("Email no registrado", 404)
    
    if password != users_db.get("password"):
        return responder("Credenciales incorrectas", 401)

    # 3. Si todo está bien, generar Token
    token = create_access_token(identity=email)

    # 4. Respuesta de éxito
    app.logger.info(f"login exitoso email={email}")
    if request.is_json:
        return jsonify(access_token=token)
    
    resp = redirect(url_for("dashboard_page"))
    set_access_cookies(resp, token)
    return resp

# Punto de entrada de la aplicación
@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/dashboard", methods=["GET"])
@jwt_required(locations=["cookies"]) # Protege la ruta: requiere token válido en la cookie
def dashboard_page():
    user = get_jwt_identity()
    app.logger.info(f"dashboard acceso user={user}")
    return render_template("dashboard/index.html", user=user)

@app.route("/logout")
def logout():
    resp = redirect(url_for("index_page"))
    unset_jwt_cookies(resp)
    app.logger.info("logout")
    return resp

@app.errorhandler(404)
def not_found(error):
    app.logger.warning(f"404 {request.path}")
    return render_template("404.html"), 404


if __name__ == "__main__":
    debug_env = os.getenv("FLASK_DEBUG", "true").lower()
    debug = debug_env in ("1", "true", "t", "yes", "y")
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5000"))
    app.run(debug=debug, host=host, port=port)
