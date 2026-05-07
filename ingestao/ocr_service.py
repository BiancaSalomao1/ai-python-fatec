# from __future__ import annotations
# import cv2
# import easyocr


# class OCRService:
#     def __init__(self):
#         self.reader = easyocr.Reader(
#             ["pt", "en"],
#             gpu=False
#         )

#         print("OCRService inicializado com EasyOCR.")

#     def preprocessar_imagem(self, caminho_imagem: str):
#         img = cv2.imread(caminho_imagem)

#         if img is None:
#             raise FileNotFoundError(
#                 f"Imagem não encontrada: {caminho_imagem}"
#             )

#         gray = cv2.cvtColor(
#             img,
#             cv2.COLOR_BGR2GRAY
#         )

#         gray = cv2.equalizeHist(gray)

#         thresh = cv2.adaptiveThreshold(
#             gray,
#             255,
#             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#             cv2.THRESH_BINARY,
#             11,
#             2
#         )

#         return thresh







#     def extrair_texto(
#         self,
#         imagem_path: str
#     ) -> list[dict]:

#         resultados = self.reader.readtext(
#             imagem_path
#         )

#         textos = []

#         for resultado in resultados:

#             textos.append({
#                 "texto": resultado[1]
#             })

#         return textos
    


#     # def extrair_texto(self, caminho_imagem: str):
#     #     img = self.preprocessar_imagem(caminho_imagem)

#     #     resultado = self.reader.readtext(img)

#     #     textos = []

#     #     for item in resultado:
#     #         textos.append({
#     #             "texto": item[1],
#     #             "confianca": float(item[2])
#     #         })

#     #     return textos
# file: ingestao/ocr_service.py

import easyocr


class OCRService:

    def __init__(self):

        self.reader = easyocr.Reader(
            ["pt"],
            gpu=False
        )

        print(
            "OCRService inicializado "
            "com EasyOCR."
        )

    def extrair_texto(
        self,
        imagem_path: str
    ) -> list[dict]:

        print(
            f"\nProcessando imagem: "
            f"{imagem_path}\n"
        )

        resultados = self.reader.readtext(
            imagem_path,
            detail=1,
            paragraph=False
        )

        print(
            f"Resultados OCR: "
            f"{len(resultados)}\n"
        )

        textos = []

        for resultado in resultados:

            print(resultado)

            texto = resultado[1].strip()

            if not texto:
                continue

            textos.append({
                "texto": texto
            })

        print(
            "\n=== TEXTOS EXTRAIDOS ===\n"
        )

        for item in textos:

            print(item)

        return textos