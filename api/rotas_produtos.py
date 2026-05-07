from flask import Blueprint
from flask import jsonify
from flask import request

from inteligencia.nlp_processor import NLPProcessor


produtos_bp = Blueprint(
    "produtos",
    __name__
)

nlp = NLPProcessor()


@produtos_bp.route(
    "/categorizar",
    methods=["POST"]
)
def categorizar():

    dados = request.get_json()

    produtos = dados.get(
        "produtos",
        []
    )

    resultado = (
        nlp.categorizar_lista(
            produtos
        )
    )

    return jsonify(resultado)


@produtos_bp.route(
    "/deduplicar",
    methods=["POST"]
)
def deduplicar():

    dados = request.get_json()

    produtos = dados.get(
        "produtos",
        []
    )

    resultado = (
        nlp.remover_duplicados(
            produtos
        )
    )

    return jsonify(resultado)