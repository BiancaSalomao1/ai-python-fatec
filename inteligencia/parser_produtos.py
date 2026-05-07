import re

class ProdutoParser:

    @staticmethod
    def extrair_produtos(textos):
        produtos = []
        produto_atual = None

        for item in textos:
            texto = item["texto"]

            match_preco = re.search(r'\d{1,3},\d{2}', texto)

            if match_preco:
                preco = float(match_preco.group().replace(',', '.'))

                if produto_atual:
                    produtos.append({
                        "produto": produto_atual,
                        "preco": preco
                    })
                    produto_atual = None
            else:
                produto_atual = texto

        return produtos