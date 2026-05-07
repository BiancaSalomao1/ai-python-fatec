import re


class OCRNormalizer:

    PALAVRAS_LIXO = {
        "OFERTA",
        "PROMOCAO",
        "PROMOÇÃO",
        "TOTAL",
        "CUPOM",
        "FISCAL",
        "ICMS",
        "CNPJ"
    }

    @staticmethod
    def limpar_textos(textos):
        resultado = []

        for item in textos:
            texto = item["texto"].strip()

            texto = re.sub(r"[^\w\s.,/-]", "", texto)

            if len(texto) <= 2:
                continue

            if texto.upper() in OCRNormalizer.PALAVRAS_LIXO:
                continue

            confianca = item.get("confianca", 0)

            if confianca < 0.35:
                continue

            resultado.append({
                "texto": texto,
                "confianca": confianca
            })

        return resultado