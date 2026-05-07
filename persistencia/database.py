from __future__ import annotations

import json
from pathlib import Path

from persistencia.models import Extracao


class Database:

    def salvar_extracao(
        self,
        extracao: Extracao,
        caminho: Path
    ):

        dados = {
            "nome_arquivo": extracao.nome_arquivo,
            "data_extracao": extracao.data_extracao,
            "produtos": extracao.produtos
        }

        with open(
            caminho,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

    def listar_extracoes(
        self,
        pasta: Path
    ) -> list[dict]:

        resultados = []

        if not pasta.exists():
            return resultados

        for arquivo in pasta.glob("*.json"):

            with open(
                arquivo,
                "r",
                encoding="utf-8"
            ) as f:

                resultados.append(
                    json.load(f)
                )

        return resultados