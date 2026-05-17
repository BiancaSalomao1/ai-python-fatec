from __future__ import annotations

from difflib import SequenceMatcher
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
        return ((preco_atual - preco_antigo) / preco_antigo) * 100

    def _nomes_similares(
        self,
        nome_a: str,
        nome_b: str,
        limite: float = 0.75
    ) -> bool:
        a = nome_a.lower().strip()
        b = nome_b.lower().strip()
        return SequenceMatcher(None, a, b).ratio() >= limite

    def anotar_variacao(
        self,
        produtos_atuais: list[dict]
    ) -> list[dict]:
        """Anota cada produto com sua variação em relação ao último preço registrado."""
        extracoes = self.database.listar_extracoes(EXTRACOES_DIR)
        extracoes.sort(key=lambda x: x.get("data_extracao", ""))

        historico: dict[str, float] = {}
        for extracao in extracoes:
            for produto in extracao.get("produtos", []):
                nome = produto.get("produto", "").strip()
                preco = produto.get("preco")
                if nome and isinstance(preco, (int, float)):
                    historico[nome] = preco

        resultado = []
        for produto in produtos_atuais:
            p = dict(produto)
            nome_atual = p.get("produto", "")
            preco_atual = p.get("preco", 0)

            for nome_hist, preco_hist in historico.items():
                if self._nomes_similares(nome_atual, nome_hist):
                    p["preco_anterior"] = preco_hist
                    p["variacao_pct"] = self.calcular_inflacao(
                        preco_hist, preco_atual
                    )
                    break

            resultado.append(p)
        return resultado

    def historico_por_produto(self) -> dict:
        """Retorna séries de preço por produto (apenas produtos com ≥2 registros)."""
        extracoes = self.database.listar_extracoes(EXTRACOES_DIR)
        extracoes.sort(key=lambda x: x.get("data_extracao", ""))

        historico: dict[str, list[dict]] = {}

        for extracao in extracoes:
            data = extracao.get("data_extracao", "")[:10]
            for produto in extracao.get("produtos", []):
                nome = produto.get("produto", "").strip()
                preco = produto.get("preco")
                if not nome or not isinstance(preco, (int, float)):
                    continue
                chave = None
                for k in historico:
                    if self._nomes_similares(nome, k):
                        chave = k
                        break
                if chave is None:
                    chave = nome
                historico.setdefault(chave, []).append({"data": data, "preco": preco})

        return {k: v for k, v in historico.items() if len(v) >= 2}

    def gerar_estatisticas(self) -> dict:
        extracoes = self.database.listar_extracoes(EXTRACOES_DIR)

        extracoes.sort(key=lambda x: x.get("data_extracao", ""))

        total_notas = len(extracoes)
        total_produtos = sum(
            len(e.get("produtos", [])) for e in extracoes
        )

        # Agrupar histórico de preços por produto (mesmo produto, notas diferentes)
        historico: dict[str, list[float]] = {}

        for extracao in extracoes:
            for produto in extracao.get("produtos", []):
                nome = produto.get("produto", "").strip()
                preco = produto.get("preco")

                if not nome or not isinstance(preco, (int, float)):
                    continue

                chave = None
                for k in historico:
                    if self._nomes_similares(nome, k):
                        chave = k
                        break

                if chave is None:
                    chave = nome

                historico.setdefault(chave, []).append(preco)

        # Calcular inflação apenas para produtos com ≥2 registros
        inflacoes = []
        for precos in historico.values():
            if len(precos) >= 2:
                inflacoes.append(
                    self.calcular_inflacao(precos[0], precos[-1])
                )

        inflacao_media = (
            sum(inflacoes) / len(inflacoes) if inflacoes else 0.0
        )

        return {
            "total_notas": total_notas,
            "total_produtos": total_produtos,
            "inflacao_media": inflacao_media,
            "produtos_rastreados": len(inflacoes),
        }
