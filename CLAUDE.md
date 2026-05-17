# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sistema de Monitoramento de Preços e Inflação — an academic project (FATEC/RP AI course) that processes Brazilian grocery receipts (notas fiscais) via OCR, extracts product/price pairs using an LLM, and tracks price trends over time.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install easyocr pillow google-genai sentence-transformers scikit-learn flask
```

Set the required environment variable before running:
```bash
export GEMINI_API_KEY=your_key_here
```

## Running

```bash
# Desktop GUI app (main entry point)
python main.py

# Manual test script (update the hardcoded image path inside the file first)
python testes/test_ocr.py
```

## Architecture

The app has four layers:

**`ingestao/`** — Data ingestion  
- `ocr_service.py` — Wraps EasyOCR (Portuguese) to extract text from receipt images as `[{"texto": str}]` lists  
- `estatistica_service.py` — Reads all saved JSON extractions and computes inflation metrics by comparing sequential prices

**`inteligencia/`** — AI processing  
- `llm_parse.py` — Primary product extractor: sends filtered OCR lines to `gemini-2.0-flash-lite` and parses the JSON response. Falls back to a local regex parser (`extrair_localmente`) automatically on HTTP 429 quota errors  
- `normalizer.py` — `OCRNormalizer`: removes low-confidence and noise tokens from raw OCR output before LLM processing  
- `parser_produtos.py` — `ProdutoParser`: pure regex fallback that pairs product names with prices by scanning adjacent lines  
- `embeddings.py` — `EmbeddingService`: wraps `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` for cosine similarity and semantic search  
- `nlp_processor.py` — `NLPProcessor`: product deduplication and categorization using a hybrid score (70% semantic embedding similarity + 30% textual SequenceMatcher ratio, threshold 0.85)

**`persistencia/`** — Storage  
- Persistence is JSON files in `persistencia/extracoes/` (one file per processed receipt), not a database  
- `database.py` — `Database`: reads/writes those JSON files  
- `models.py` — `Extracao` dataclass (filename, products list, timestamp)

**`api/`** — Flask blueprints (not yet wired to `main.py`)  
- `rotas_ocr.py` — `POST /processar` — runs LLM parsing on posted OCR texts  
- `rotas_comparacao.py` — `POST /similaridade` — returns cosine similarity score between two product names  
- `rotas_produtos.py` — `POST /categorizar`, `POST /deduplicar` — NLP product operations  
- `rotas_dashboard.py` — `GET /health`, `GET /info`

## Known Issues

- `main.py` imports from `services.ocr_service` and `services.estatistica_service`, but those modules live in `ingestao/`. These import paths are broken and need to be corrected to `ingestao.ocr_service` and `ingestao.estatistica_service`.
- The README describes FastAPI, PaddleOCR+YOLO, and PostgreSQL+pgvector — the actual implementation uses Flask, EasyOCR, and local JSON files.
- `testes/test_ocr.py` has a hardcoded absolute image path that must be updated before running.
- There is no `requirements.txt` in the repository.
