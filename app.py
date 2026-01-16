# run.py

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Importar la base de datos
from database import db

# Importar modelos individuales
from models.usuario_model import Usuario
from models.producto_model import Producto
from models.carrito_model import Carrito
from models.compra_model import Compra
from models.detalle_compra_model import DetalleCompra
from models.categoria_model import Categoria
from models.comentario_model import Comentario
from models.favorito_model import Favorito
from models.mensaje_model import Mensaje

# Inicializaciones
migrate = Migrate()
login_manager = LoginManager()

# Crear la app Flask
app = Flask(__name__)
app.secret_key = "clave_segura"

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pymemarket.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear carpeta 'instance' si no existe
os.makedirs("instance", exist_ok=True)

# Inicializar extensiones
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = "auth.login"  # Ruta por defecto si no estás logueado

# Crear tablas si no existen
with app.app_context():
    db.create_all()

# Ruta principal de prueba
@app.route("/")
def home():
    return "¡PymeMarket está vivo!"

# Cargar usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Registrar Blueprints
from controllers.auth_controller import auth_blueprint
from controllers.producto_controller import producto_blueprint
from controllers.carrito_controller import carrito_blueprint
from controllers.usuario_controller import usuario_blueprint
from controllers.categoria_controller import categoria_blueprint
from controllers.favorito_controller import favorito_blueprint
from controllers.comentario_controller import comentario_blueprint
from controllers.detalle_compra_controller import detalle_compra_blueprint
from controllers.direccion_envio_controller import direccion_envio_blueprint
from controllers.compra_controller import compra_blueprint
from controllers.mensaje_controller import mensaje_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(producto_blueprint)
app.register_blueprint(carrito_blueprint)
app.register_blueprint(usuario_blueprint)
app.register_blueprint(categoria_blueprint)
app.register_blueprint(favorito_blueprint)
app.register_blueprint(comentario_blueprint)
app.register_blueprint(detalle_compra_blueprint)
app.register_blueprint(direccion_envio_blueprint)
app.register_blueprint(compra_blueprint)
app.register_blueprint(mensaje_blueprint)


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
