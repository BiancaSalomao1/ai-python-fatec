# file: testes/test_ocr.py

import sys
from pathlib import Path

import cv2
import numpy as np



ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT))

from inteligencia.llm_parse import LLMParser
from inteligencia.normalizer import OCRNormalizer
from ingestao.ocr_service import OCRService

def main():

    print(
        f"Numpy: {np.__version__}"
    )

    print(
        f"OpenCV: {cv2.__version__}"
    )

    imagem_path = Path(
    "/home/biancav15/Documentos/Workspaces/"
    "Python/ProjetoIA/ai-python-fatec/"
    "imagens/NF01.jpeg"
)

    if not imagem_path.exists():

        raise FileNotFoundError(
            f"Imagem não encontrada: {imagem_path}"
        )

    ocr = OCRService()

    textos = ocr.extrair_texto(
        str(imagem_path)
    )

    textos_limpos = textos
        
    

    parser = LLMParser()

    produtos = (
        parser.estruturar_produtos(
            textos_limpos
        )
    )
    if isinstance(produtos, dict):

        print(
        "\n=== ERRO ===\n"
    )

        print(produtos)

    return


    print(
        "\n=== PRODUTOS EXTRAIDOS ===\n"
    )

    for produto in produtos:

        print(produto)


if __name__ == "__main__":

    main()