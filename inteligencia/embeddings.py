# file: inteligencia/embeddings.py

from __future__ import annotations

from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingService:

    def __init__(
        self,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ) -> None:

        self.model = SentenceTransformer(
            model_name
        )

    def gerar_embedding(
        self,
        texto: str
    ) -> np.ndarray:

        embedding = self.model.encode(
            texto,
            convert_to_numpy=True
        )

        return embedding

    def gerar_embeddings(
        self,
        textos: List[str]
    ) -> np.ndarray:

        embeddings = self.model.encode(
            textos,
            convert_to_numpy=True
        )

        return embeddings

    def similaridade(
        self,
        texto_1: str,
        texto_2: str
    ) -> float:

        emb_1 = self.gerar_embedding(
            texto_1
        )

        emb_2 = self.gerar_embedding(
            texto_2
        )

        score = cosine_similarity(
            [emb_1],
            [emb_2]
        )[0][0]

        return float(score)

    def buscar_similares(
        self,
        consulta: str,
        textos: List[str],
        top_k: int = 5
    ) -> List[dict]:

        emb_consulta = self.gerar_embedding(
            consulta
        )

        emb_textos = self.gerar_embeddings(
            textos
        )

        scores = cosine_similarity(
            [emb_consulta],
            emb_textos
        )[0]

        resultados = []

        for texto, score in zip(
            textos,
            scores
        ):

            resultados.append({
                "texto": texto,
                "score": float(score)
            })

        resultados.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return resultados[:top_k]