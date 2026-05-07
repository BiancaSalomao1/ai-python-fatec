from flask import Flask

from api.rotas_comparacao import comparacao_bp
from api.rotas_dashboard import dashboard_bp
from api.rotas_ocr import ocr_bp
from api.rotas_produtos import produtos_bp


def criar_app() -> Flask:

    app = Flask(__name__)

    app.register_blueprint(
        comparacao_bp,
        url_prefix="/comparacao"
    )

    app.register_blueprint(
        dashboard_bp,
        url_prefix="/dashboard"
    )

    app.register_blueprint(
        ocr_bp,
        url_prefix="/ocr"
    )

    app.register_blueprint(
        produtos_bp,
        url_prefix="/produtos"
    )

    return app