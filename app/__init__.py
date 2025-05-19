# app/__init__.py
from flask import Flask
from .routes import bp
from .generate_dataset import gerar_dataset_se_nao_existir

def create_app():
    gerar_dataset_se_nao_existir()  
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app
