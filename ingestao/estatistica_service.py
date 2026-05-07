from __future__ import annotations

from pathlib import Path

from persistencia.database import Database


BASE_DIR = Path(__file__).resolve().parent.parent
EXTRACOES_DIR = BASE_DIR / "persistencia" / "extracoes"


class EstatisticaService:

    def __init__(
        self,
        database: Database
    ):

        self.database = database

    def calcular_inflacao(
        self,
        preco_antigo: float,
        preco_atual: float
    ) -> float:

        if preco_antigo <= 0:
            return 0

        return (
            (
                preco_atual - preco_antigo
            ) / preco_antigo
        ) * 100

    def gerar_estatisticas(
        self
    ) -> dict:

        extracoes = (
            self.database
            .listar_extracoes(
                EXTRACOES_DIR
            )
        )

        total_notas = len(
            extracoes
        )

        total_produtos = 0

        precos = []

        for extracao in extracoes:

            produtos = extracao.get(
                "produtos",
                []
            )

            total_produtos += len(
                produtos
            )

            for produto in produtos:

                preco = produto.get(
                    "preco"
                )

                if isinstance(
                    preco,
                    (int, float)
                ):

                    precos.append(preco)

        inflacao_media = 0

        if len(precos) >= 2:

            inflacoes = []

            for i in range(
                1,
                len(precos)
            ):

                inflacao = (
                    self.calcular_inflacao(
                        precos[i - 1],
                        precos[i]
                    )
                )

                inflacoes.append(
                    inflacao
                )

            if inflacoes:

                inflacao_media = (
                    sum(inflacoes)
                    / len(inflacoes)
                )

        return {
            "total_notas": total_notas,
            "total_produtos": total_produtos,
            "inflacao_media": inflacao_media
        }
