from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from api.rotas_dashboard import dashboard_bp
from ingestao.estatistica_service import EstatisticaService
from ingestao.ocr_service import OCRService
from inteligencia.llm_parse import LLMParser
from inteligencia.nlp_processor import NLPProcessor
from inteligencia.normalizer import OCRNormalizer
from persistencia.database import Database
from persistencia.models import Extracao

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "imagens"
EXTRACOES_DIR = BASE_DIR / "persistencia" / "extracoes"

UPLOAD_DIR.mkdir(exist_ok=True)
EXTRACOES_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

app.register_blueprint(dashboard_bp)

_db = Database()
_ocr = OCRService()
_llm = LLMParser()
_nlp = NLPProcessor()
_est = EstatisticaService(_db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "imagem" not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    arquivo = request.files["imagem"]
    if not arquivo.filename:
        return jsonify({"erro": "Arquivo sem nome"}), 400

    nome = secure_filename(arquivo.filename)
    caminho = UPLOAD_DIR / nome
    arquivo.save(caminho)

    textos_ocr = _ocr.extrair_texto(str(caminho))
    textos_ocr = OCRNormalizer.limpar_textos(textos_ocr)
    produtos = _llm.estruturar_produtos(textos_ocr)

    if isinstance(produtos, list):
        produtos = _nlp.remover_duplicados(produtos)
        produtos = _nlp.categorizar_lista(produtos)
        produtos = _est.anotar_variacao(produtos)

    lista = produtos if isinstance(produtos, list) else []

    _db.salvar_extracao(
        Extracao(nome_arquivo=nome, produtos=lista),
        EXTRACOES_DIR / f"{caminho.stem}.json",
    )

    return jsonify({
        "produtos": lista,
        "estatisticas": _est.gerar_estatisticas(),
    })


@app.route("/estatisticas")
def estatisticas():
    return jsonify(_est.gerar_estatisticas())


@app.route("/historico")
def historico():
    return jsonify(_est.historico_por_produto())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
