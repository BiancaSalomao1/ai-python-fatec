from flask import Blueprint
from flask import jsonify
from flask import request

from inteligencia.embeddings import EmbeddingService


comparacao_bp = Blueprint(
    "comparacao",
    __name__
)

embedding_service = (
    EmbeddingService()
)


@comparacao_bp.route(
    "/similaridade",
    methods=["POST"]
)
def comparar():

    dados = request.get_json()

    texto_1 = dados.get(
        "texto_1",
        ""
    )

    texto_2 = dados.get(
        "texto_2",
        ""
    )

    score = (
        embedding_service.similaridade(
            texto_1,
            texto_2
        )
    )

    return jsonify({
        "similaridade": score
    })