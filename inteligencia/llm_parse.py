import json
import os
import re
from typing import Any

from google import genai
from google.genai import types


class LLMParser:

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "Variável de ambiente "
                "GEMINI_API_KEY "
                "não encontrada."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def extrair_localmente(
        self,
        linhas: list[str]
    ) -> list[dict]:

        produtos = []

        palavras_ignoradas = [
            "cnpj",
            "cpf",
            "subtotal",
            "total",
            "tributo",
            "valor",
            "credito",
            "pix",
            "cartao",
            "protocolo",
            "consulta",
            "serie",
            "emisso",
        ]

        linhas_validas = []

        for linha in linhas:

            linha = linha.strip()

            if not linha:
                continue

            linha_lower = linha.lower()

            if any(
                palavra in linha_lower
                for palavra in palavras_ignoradas
            ):
                continue

            linhas_validas.append(
                linha
            )

        i = 0

        while i < len(linhas_validas):

            linha = linhas_validas[i]

            possui_preco = re.search(
                r"\d+[\.,]\d{2}",
                linha
            )

            if (
                not possui_preco and
                len(linha) > 8
            ):

                nome_produto = linha

                preco = None

                for j in range(
                    i + 1,
                    min(i + 4, len(linhas_validas))
                ):

                    prox_linha = (
                        linhas_validas[j]
                    )

                    matches = re.findall(
                        r"\d+[\.,]\d{2}",
                        prox_linha
                    )

                    if not matches:
                        continue

                    try:

                        preco = float(
                            matches[-1]
                            .replace(",", ".")
                        )

                        break

                    except ValueError:
                        continue

                if preco:

                    nome_produto = re.sub(
                        r"^\d+",
                        "",
                        nome_produto
                    )

                    nome_produto = re.sub(
                        r"[^A-Za-zÀ-ÿ0-9\s]",
                        "",
                        nome_produto
                    )

                    nome_produto = re.sub(
                        r"\s+",
                        " ",
                        nome_produto
                    ).strip()

                    if len(nome_produto) >= 4:

                        produtos.append({
                            "produto": (
                                nome_produto.upper()
                            ),
                            "preco": preco
                        })

            i += 1

        produtos_unicos = []

        vistos = set()

        for produto in produtos:

            chave = (
                produto["produto"],
                produto["preco"]
            )

            if chave in vistos:
                continue

            vistos.add(chave)

            produtos_unicos.append(
                produto
            )

        return produtos_unicos

    def estruturar_produtos(
        self,
        textos: list[dict[str, Any]]
    ) -> list[dict[str, Any]] | dict[str, str]:

        linhas: list[str] = []

        for item in textos:

            texto = item.get(
                "texto",
                ""
            ).strip()

            if texto:
                linhas.append(texto)

        linhas_filtradas = []

        palavras_lixo = [
            "cnpj",
            "cpf",
            "ie:",
            "tributo",
            "tributos",
            "protocolo",
            "consulta",
            "chave",
            "autorizacao",
            "consumidor",
            "serie",
            "emisso",
            "ecf",
            "operador",
            "cartao",
            "credito",
            "debito",
            "pix",
            "visa",
            "master",
            "dinheiro",
            "troco",
            "subtotal",
        ]

        for linha in linhas:

            linha = linha.strip()

            if not linha:
                continue

            linha_lower = linha.lower()

            if any(
                palavra in linha_lower
                for palavra in palavras_lixo
            ):
                continue

            if re.fullmatch(
                r"[0-9\s\.,/-]+",
                linha
            ):
                continue

            if len(linha) < 3:
                continue

            linhas_filtradas.append(
                linha
            )

        texto_bruto = "\n".join(
            linhas_filtradas[:40]
        )

        prompt = f"""
Você é especialista em OCR de nota fiscal brasileira.

Extraia SOMENTE produtos válidos e seus preços.

Retorne APENAS JSON válido.

Formato:
[
    {{
        "produto": "ARROZ",
        "preco": 25.90
    }}
]

Texto OCR:
{texto_bruto}
"""

        try:

            response = (
                self.client.models
                .generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0
                    )
                )
            )

            conteudo = (
                response.text.strip()
            )

            conteudo = re.sub(
                r"^```json|^```|```$",
                "",
                conteudo,
                flags=re.MULTILINE
            ).strip()

            return json.loads(
                conteudo
            )

        except Exception as e:

            print(
                "\n=== ERRO GEMINI ===\n"
            )

            print(str(e))

            if "429" in str(e):

                print(
                    "\nQuota Gemini excedida. "
                    "Usando parser local...\n"
                )

                print(
                    "\n=== LINHAS OCR ===\n"
                )

                for linha in linhas_filtradas:

                    print(linha)

                resultado_local = (
                    self.extrair_localmente(
                        linhas_filtradas
                    )
                )

                print(
                    "\n=== RESULTADO LOCAL ===\n"
                )

                import json

                print(
                    json.dumps(
                        resultado_local,
                        indent=4,
                        ensure_ascii=False
                    )
                )

                return resultado_local

            return {
                "erro": str(e)
            }