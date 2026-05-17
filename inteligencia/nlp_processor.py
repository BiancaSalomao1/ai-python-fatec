from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import List

from inteligencia.embeddings import EmbeddingService


class NLPProcessor:

    def __init__(self) -> None:

        self.embedding_service = (
            EmbeddingService()
        )

        self.categorias = {
            # alimentos
            "arroz": "alimentos",
            "feijao": "alimentos",
            "macarrao": "alimentos",
            "farinha": "alimentos",
            "acucar": "alimentos",
            "sal": "alimentos",
            "oleo": "alimentos",
            "azeite": "alimentos",
            "manteiga": "alimentos",
            "margarina": "alimentos",
            "leite": "alimentos",
            "queijo": "alimentos",
            "iogurte": "alimentos",
            "pao": "alimentos",
            "biscoito": "alimentos",
            "bolacha": "alimentos",
            "frango": "alimentos",
            "carne": "alimentos",
            "atum": "alimentos",
            "sardinha": "alimentos",
            "molho": "alimentos",
            "extrato": "alimentos",
            "tempero": "alimentos",
            "linguica": "alimentos",
            "presunto": "alimentos",
            "mortadela": "alimentos",
            "ovos": "alimentos",
            "ovo": "alimentos",
            # bebidas
            "coca": "bebidas",
            "guarana": "bebidas",
            "suco": "bebidas",
            "agua": "bebidas",
            "cerveja": "bebidas",
            "vinho": "bebidas",
            "refrigerante": "bebidas",
            "cafe": "bebidas",
            "cha": "bebidas",
            # limpeza
            "sabao": "limpeza",
            "detergente": "limpeza",
            "desinfetante": "limpeza",
            "multiuso": "limpeza",
            "amaciante": "limpeza",
            "limpador": "limpeza",
            "esponja": "limpeza",
            "alvejante": "limpeza",
            # higiene
            "shampoo": "higiene",
            "sabonete": "higiene",
            "desodorante": "higiene",
            "creme": "higiene",
            "papel": "higiene",
            "escova": "higiene",
            "pasta": "higiene",
            "absorvente": "higiene",
            "fralda": "higiene",
            "barbear": "higiene",
        }

    def normalizar_produto(
        self,
        nome: str
    ) -> str:

        nome = nome.lower().strip()

        nome = re.sub(
            r"[^a-zA-Z0-9\s]",
            "",
            nome
        )

        nome = re.sub(
            r"\s+",
            " ",
            nome
        )

        return nome

    def similaridade_textual(
        self,
        texto_1: str,
        texto_2: str
    ) -> float:

        texto_1 = self.normalizar_produto(
            texto_1
        )

        texto_2 = self.normalizar_produto(
            texto_2
        )

        return SequenceMatcher(
            None,
            texto_1,
            texto_2
        ).ratio()

    def produtos_semelhantes(
        self,
        produto_1: str,
        produto_2: str,
        limite: float = 0.85
    ) -> bool:

        similaridade_semantica = (
            self.embedding_service.similaridade(
                produto_1,
                produto_2
            )
        )

        similaridade_texto = (
            self.similaridade_textual(
                produto_1,
                produto_2
            )
        )

        score_final = (
            similaridade_semantica * 0.7 +
            similaridade_texto * 0.3
        )

        return score_final >= limite

    def remover_duplicados(
        self,
        produtos: List[dict]
    ) -> List[dict]:

        resultado = []

        for produto in produtos:

            nome_atual = produto.get(
                "produto",
                ""
            )

            duplicado = False

            for existente in resultado:

                nome_existente = existente.get(
                    "produto",
                    ""
                )

                if self.produtos_semelhantes(
                    nome_atual,
                    nome_existente
                ):

                    duplicado = True
                    break

            if not duplicado:
                resultado.append(produto)

        return resultado

    def categorizar_produto(
        self,
        nome_produto: str
    ) -> str:

        nome = self.normalizar_produto(
            nome_produto
        )

        for palavra, categoria in (
            self.categorias.items()
        ):

            if palavra in nome:
                return categoria

        return "outros"

    def categorizar_lista(
        self,
        produtos: List[dict]
    ) -> List[dict]:

        resultado = []

        for produto in produtos:

            nome = produto.get(
                "produto",
                ""
            )

            categoria = (
                self.categorizar_produto(
                    nome
                )
            )

            produto["categoria"] = (
                categoria
            )

            resultado.append(
                produto
            )

        return resultado