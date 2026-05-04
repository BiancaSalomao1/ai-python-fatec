# ai-python-fatec
#### Projeto Requisito Para Conclusão Da Disciplina De Inteligência Artificial FATEC/RP
A ser Desenvolvido em Grupo


# Sistema de Monitoramento de Preços e Inflação

Um sistema inteligente desenvolvido em Python para coleta, processamento e análise de preços no varejo.

Combina técnicas modernas como:

- IA Generativa (LLMs)
- Web Scraping
- OCR (Reconhecimento Óptico de Caracteres)
- Embeddings semânticos

O objetivo é transformar dados brutos (panfletos e sites) em insights estruturados sobre inflação e variação de preços.

## Visão Geral

O sistema realiza:

Coleta de dados
Panfletos (imagem/PDF)
Sites de supermercados
Processamento inteligente
Extração de texto (OCR)
Normalização de produtos via IA
Geração de embeddings
Análise e consulta
Comparação semântica de produtos
Monitoramento de inflação
API para consumo externo

## Arquitetura

Arquitetura modular inspirada em microsserviços:

 Estrutura do Projeto
 
monitoramento_precos/

│
├── ingestao/               
│   ├── ocr_service.py      
│   └── scraper_service.py  
│
├── inteligencia/           
│   ├── nlp_processor.py    
│   ├── normalizer.py       
│   └── embeddings.py       
│
├── persistencia/           
│   ├── database.py         
│   └── models.py           
│
├── api/                    
│   ├── rotas_comparacao.py 
│   └── rotas_dashboard.py  
│
├── main.py                 
└── requirements.txt        

## Componentes Principais
- Ingestão de Dados
OCR com PaddleOCR + YOLO
Scraping dinâmico com Playwright
Extração de pares (produto, preço)
-Inteligência Artificial
Normalização com LLMs
Exemplo:
"Arroz T1 5kg" → "Arroz Tipo 1 5kg"
Geração de embeddings para busca semântica
-Persistência
Banco PostgreSQL
Extensão pgvector
-Suporte a:
Busca por similaridade
Consultas vetoriais rápidas

## API & Interface

API construída com FastAPI
Dois focos principais:

- Dashboard de inflação
- Comparação de preços
  
## Setup Inicial
1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
2. Instalar dependências
pip install fastapi uvicorn playwright paddleocr sqlalchemy pgvector
3. Rodar aplicação
uvicorn main:app --reload

## Possibilidades Futuras
- Previsão de inflação com Machine Learning
- Integração com múltiplas redes de supermercados
- Aplicação mobile
- Alertas de variação de preços
- Diferenciais do Projeto
Uso de IA Generativa aplicada a dados reais
Busca semântica, não apenas textual
Arquitetura escalável e modular
Aplicação direta em economia e varejo
