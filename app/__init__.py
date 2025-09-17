from flask import Flask
from .extensions import db, migrate, jwt
from .routes import register_routes
from app import models  # Importa todos os modelos para garantir que sejam registrados
import os

def create_app(config_name="development"):
    app = Flask(__name__)

    # Carrega config de app/config.py
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")

    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Registra rotas
    register_routes(app)

    return app
