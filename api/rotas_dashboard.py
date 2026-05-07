from flask import Blueprint
from flask import jsonify


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route(
    "/health",
    methods=["GET"]
)
def health():

    return jsonify({
        "status": "online",
        "servico": "OCR IA API"
    })


@dashboard_bp.route(
    "/info",
    methods=["GET"]
)
def info():

    return jsonify({
        "ocr": "EasyOCR",
        "llm": "Gemini",
        "nlp": "SentenceTransformers"
    })