"""
Teste manual do pipeline OCR → Normalizer → LLM.

Uso:
    python testes/test_ocr.py imagens/NF01.jpeg
    python testes/test_ocr.py          # usa a primeira imagem encontrada em imagens/
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ingestao.ocr_service import OCRService
from inteligencia.llm_parse import LLMParser
from inteligencia.normalizer import OCRNormalizer


def main():
    # Resolve o caminho da imagem
    if len(sys.argv) > 1:
        imagem_path = Path(sys.argv[1])
    else:
        imagens = sorted((ROOT / "imagens").glob("*.jpeg")) + \
                  sorted((ROOT / "imagens").glob("*.jpg")) + \
                  sorted((ROOT / "imagens").glob("*.png"))
        if not imagens:
            print("Nenhuma imagem encontrada em imagens/. Passe o caminho como argumento.")
            sys.exit(1)
        imagem_path = imagens[0]

    if not imagem_path.exists():
        print(f"Imagem não encontrada: {imagem_path}")
        sys.exit(1)

    print(f"Imagem: {imagem_path}\n")

    # OCR
    ocr = OCRService()
    textos = ocr.extrair_texto(str(imagem_path))
    print(f"Textos brutos: {len(textos)} linhas")

    # Normalização
    textos_limpos = OCRNormalizer.limpar_textos(textos)
    print(f"Após normalização: {len(textos_limpos)} linhas\n")

    # LLM
    parser = LLMParser()
    produtos = parser.estruturar_produtos(textos_limpos)

    if isinstance(produtos, dict):
        print(f"Erro: {produtos}")
        return

    print(f"=== PRODUTOS EXTRAÍDOS ({len(produtos)}) ===\n")
    for p in produtos:
        nome = p.get("produto", "")
        preco = p.get("preco", 0)
        print(f"  {nome}: R$ {preco:.2f}")


if __name__ == "__main__":
    main()
