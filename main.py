from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image
from PIL import ImageTk

from inteligencia.llm_parse import LLMParser
from persistencia.database import Database
from persistencia.models import Extracao
from services.estatistica_service import EstatisticaService
from services.ocr_service import OCRService


BASE_DIR = Path(__file__).resolve().parent
IMAGENS_DIR = BASE_DIR / "imagens"
EXTRACOES_DIR = BASE_DIR / "persistencia" / "extracoes"

IMAGENS_DIR.mkdir(exist_ok=True)
EXTRACOES_DIR.mkdir(parents=True, exist_ok=True)


class OCRApp:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("OCR Inteligente")
        self.root.geometry("1000x700")

        self.database = Database()
        self.ocr_service = OCRService()
        self.llm_parser = LLMParser()
        self.estatistica_service = EstatisticaService(
            self.database
        )

        self.imagem_label = tk.Label(
            self.root
        )

        self.imagem_label.pack(
            pady=10
        )

        self.texto_saida = tk.Text(
            self.root,
            height=25,
            width=120
        )

        self.texto_saida.pack(
            pady=10
        )

        botao_upload = tk.Button(
            self.root,
            text="Selecionar Nota Fiscal",
            command=self.processar_imagem,
            height=2,
            width=30
        )

        botao_upload.pack(
            pady=10
        )

    def mostrar_imagem(
        self,
        caminho: Path
    ):

        imagem = Image.open(caminho)

        imagem.thumbnail((400, 400))

        imagem_tk = ImageTk.PhotoImage(imagem)

        self.imagem_label.configure(
            image=imagem_tk
        )

        self.imagem_label.image = imagem_tk

    def processar_imagem(self):

        caminho = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[
                (
                    "Imagens",
                    "*.png *.jpg *.jpeg"
                )
            ]
        )

        if not caminho:
            return

        caminho_original = Path(caminho)

        destino = IMAGENS_DIR / caminho_original.name

        destino.write_bytes(
            caminho_original.read_bytes()
        )

        self.mostrar_imagem(destino)

        textos_ocr = self.ocr_service.extrair_texto(
            str(destino)
        )

        produtos = (
            self.llm_parser.estruturar_produtos(
                textos_ocr
            )
        )

        extracao = Extracao(
            nome_arquivo=destino.name,
            produtos=produtos
        )

        caminho_json = (
            EXTRACOES_DIR /
            f"{destino.stem}.json"
        )

        self.database.salvar_extracao(
            extracao,
            caminho_json
        )

        estatisticas = (
            self.estatistica_service
            .gerar_estatisticas()
        )

        self.texto_saida.delete(
            "1.0",
            tk.END
        )

        self.texto_saida.insert(
            tk.END,
            "=== PRODUTOS EXTRAIDOS ===\n\n"
        )

        for produto in produtos:

            self.texto_saida.insert(
                tk.END,
                f"{produto}\n"
            )

        self.texto_saida.insert(
            tk.END,
            "\n=== ESTATISTICAS ===\n\n"
        )

        self.texto_saida.insert(
            tk.END,
            f"Total de notas: {estatisticas['total_notas']}\n"
        )

        self.texto_saida.insert(
            tk.END,
            f"Total produtos: {estatisticas['total_produtos']}\n"
        )

        self.texto_saida.insert(
            tk.END,
            f"Inflacao media: {estatisticas['inflacao_media']:.2f}%\n"
        )

        messagebox.showinfo(
            "Sucesso",
            "OCR processado com sucesso"
        )

    def executar(self):

        self.root.mainloop()


if __name__ == "__main__":

    app = OCRApp()

    app.executar()



