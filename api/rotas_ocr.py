from flask import Blueprint
from flask import jsonify
from flask import request

from inteligencia.llm_parse import LLMParser


ocr_bp = Blueprint(
    "ocr",
    __name__
)


@ocr_bp.route(
    "/processar",
    methods=["POST"]
)
def processar_ocr():

    dados = request.get_json()

    textos = dados.get(
        "textos",
        []
    )

    parser = LLMParser()

    resultado = (
        parser.estruturar_produtos(
            textos
        )
    )

    return jsonify(resultado)