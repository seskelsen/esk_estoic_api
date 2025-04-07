from fastapi import FastAPI, Query, HTTPException, status, Path as FastAPIPath
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import List, Optional
from random import choice
from datetime import datetime
from zoneinfo import ZoneInfo
from .data.quotes import quotes
import uvicorn
import asyncio
import os
from pathlib import Path
from contextlib import asynccontextmanager

# Modelos de dados para a documentação
class QuoteBase(BaseModel):
    text: str = Field(..., description="O texto da citação estoica", example="A vida é curta, mas a arte é longa.")
    author: str = Field(..., description="O autor da citação", example="Sêneca")
    date: str = Field(..., description="A data associada à citação no formato MM-DD", example="01-01")

class QuoteResponse(QuoteBase):
    class Config:
        json_schema_extra = {
            "example": {
                "text": "A vida é curta, mas a arte é longa.",
                "author": "Sêneca",
                "date": "01-01"
            }
        }

class QuoteEnglish(QuoteBase):
    text: str = Field(..., description="O texto da citação estoica em inglês", example="Life is short, but art is long.")
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Life is short, but art is long.",
                "author": "Seneca",
                "date": "01-01"
            }
        }

class Error(BaseModel):
    detail: str = Field(..., description="Detalhes do erro")

# Obtenha o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações de ambiente
ENV = os.getenv("APP_ENV", "development")
DEBUG = ENV == "development"
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Cleanup on shutdown
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

# Configuração do aplicativo FastAPI com documentação aprimorada
app = FastAPI(
    title="API de Citações Estoicas",
    description="""
    # API de Citações Estoicas
    
    Esta API fornece acesso a uma coleção de citações da filosofia estoica, disponíveis em português e inglês.
    
    ## Funcionalidades
    
    * Obtenha a citação do dia atual
    * Receba uma citação aleatória
    * Busque citações por autor
    * Acesse todas as citações disponíveis
    
    ## Informações
    
    A API contém citações para todos os 366 dias do ano (incluindo 29 de fevereiro).
    Todas as citações estão disponíveis em português e inglês.
    """,
    version="1.1.0",
    lifespan=lifespan,
    debug=DEBUG,
    contact={
        "name": "Desenvolvedor",
        "url": "https://github.com/seu-usuario/esk_estoic_api",
        "email": "seu-email@exemplo.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    terms_of_service="https://github.com/seu-usuario/esk_estoic_api",
)

# Configure CORS
allowed_origins = ["http://localhost:3000", "http://localhost:5000", "http://localhost:8000", "*"]

# Em produção, permitir configurar as origens por variável de ambiente
if ENV == "production":
    # As origens podem ser definidas como uma lista separada por vírgulas
    prod_origins = os.getenv("ALLOWED_ORIGINS", "*")
    if prod_origins != "*":
        allowed_origins = prod_origins.split(",")
    else:
        # Em produção, permitimos todas as origens
        allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "X-Content-Type-Options"],
    max_age=3600,
)

# Mount static files directory to serve CSS and JavaScript files
static_dir = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
async def read_root():
    index_path = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index_path)

@app.get(
    "/quote/today", 
    response_model=QuoteResponse, 
    responses={404: {"model": Error, "description": "Citação não encontrada"}},
    summary="Obter a citação do dia",
    description="""
    Retorna a citação estoica correspondente à data atual.
    
    A data é determinada pelo fuso horário brasileiro (America/Sao_Paulo).
    Se não houver uma citação específica para o dia atual, o sistema encontrará a próxima citação disponível.
    """,
    tags=["Citações em Português"]
)
async def get_today_quote():
    # Get current date in Brazilian timezone
    today = datetime.now(ZoneInfo("America/Sao_Paulo"))
    today_date = today.strftime("%m-%d")
    
    # Find quote for today's date
    for quote in quotes:
        if quote["date"] == today_date:
            return {"text": quote["text"], "author": quote["author"], "date": quote["date"]}
    
    # If no quote found for today, find the next available quote
    # Convert today's date to a number (e.g., 0101 for January 1)
    today_num = int(today_date.replace('-', ''))
    
    # Find the quote with the closest next date
    available_dates = [(int(q['date'].replace('-', '')), q) for q in quotes]
    available_dates.sort()
    
    # Find the next available date
    next_quote = None
    for date_num, quote in available_dates:
        if date_num >= today_num:
            next_quote = quote
            break
    
    # If no next quote found (we're at the end of the year), take the first quote of the year
    if not next_quote:
        next_quote = available_dates[0][1]
    
    return {"text": next_quote["text"], "author": next_quote["author"], "date": next_quote["date"]}

@app.get(
    "/quote/today/en", 
    response_model=QuoteEnglish, 
    responses={404: {"model": Error, "description": "Citação não encontrada"}},
    summary="Obter a citação do dia em inglês",
    description="""
    Retorna a citação estoica correspondente à data atual em inglês.
    
    A data é determinada pelo fuso horário brasileiro (America/Sao_Paulo).
    Se não houver uma citação específica para o dia atual, o sistema usará um método determinístico para selecionar uma citação.
    """,
    tags=["Citações em Inglês"]
)
async def get_today_quote_english():
    # Get current date in Brazilian timezone
    today = datetime.now(ZoneInfo("America/Sao_Paulo"))
    today_date = today.strftime("%m-%d")
    
    # Find quote for today's date
    for quote in quotes:
        if quote["date"] == today_date:
            return {"text": quote["text_en"], "author": quote["author"], "date": quote["date"]}
    
    # If no quote found for today, use a deterministic approach based on the date
    day_of_year = int(today.strftime("%j"))
    quote_index = day_of_year % len(quotes)
    quote = quotes[quote_index]
    return {"text": quote["text_en"], "author": quote["author"], "date": quote["date"]}

@app.get(
    "/quote/random", 
    response_model=QuoteResponse,
    summary="Obter uma citação aleatória",
    description="Retorna uma citação estoica aleatória em português do banco de dados de citações.",
    tags=["Citações em Português"]
)
async def get_random_quote():
    quote = choice(quotes)
    return {"text": quote["text"], "author": quote["author"], "date": quote["date"]}

@app.get(
    "/quote/random/en", 
    response_model=QuoteEnglish,
    summary="Obter uma citação aleatória em inglês",
    description="Retorna uma citação estoica aleatória em inglês do banco de dados de citações.",
    tags=["Citações em Inglês"]
)
async def get_random_quote_english():
    quote = choice(quotes)
    return {"text": quote["text_en"], "author": quote["author"], "date": quote["date"]}

@app.get(
    "/quotes", 
    response_model=List[QuoteResponse],
    summary="Listar todas as citações",
    description="""
    Retorna a lista completa de todas as citações estoicas disponíveis no banco de dados.
    
    Esta chamada pode retornar um grande volume de dados, pois inclui citações para todos os 366 dias do ano.
    """,
    tags=["Coleções"]
)
async def get_all_quotes():
    return quotes

@app.get(
    "/quotes/{author}", 
    response_model=List[QuoteResponse], 
    responses={404: {"model": Error, "description": "Autor não encontrado"}},
    summary="Buscar citações por autor",
    description="""
    Retorna todas as citações de um autor específico.
    
    A busca não é sensível a maiúsculas e minúsculas.
    Se nenhuma citação for encontrada para o autor especificado, retorna uma mensagem de erro 404.
    """,
    tags=["Coleções"]
)
async def get_quotes_by_author(
    author: str = FastAPIPath(
        ..., 
        description="O nome do autor das citações", 
        example="Sêneca"
    )
):
    author_quotes = [quote for quote in quotes if quote["author"].lower() == author.lower()]
    if not author_quotes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Autor '{author}' não encontrado"
        )
    return author_quotes

# Personalização da documentação OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Customização adicional do esquema OpenAPI
    openapi_schema["info"]["x-logo"] = {
        "url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg",
        "backgroundColor": "#FFFFFF",
        "altText": "API de Citações Estoicas Logo"
    }
    
    # Adiciona exemplos mais detalhados
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    if "examples" not in openapi_schema["components"]:
        openapi_schema["components"]["examples"] = {}
    
    openapi_schema["components"]["examples"]["QuoteExample"] = {
        "value": {
            "text": "O sucesso vem para aqueles que se preparam para ele.",
            "author": "Epictetus",
            "date": "04-04"
        },
        "summary": "Exemplo de citação estoica"
    }
    
    openapi_schema["components"]["examples"]["QuoteEnglishExample"] = {
        "value": {
            "text": "Success comes to those who prepare for it.",
            "author": "Epictetus",
            "date": "04-04"
        },
        "summary": "Exemplo de citação estoica em inglês"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    # Configure uvicorn with optimized settings for development
    config = uvicorn.Config(
        "src.main:app",
        host=HOST,
        port=PORT,
        workers=1,  # Single worker for development
        limit_concurrency=100,  # Balanced concurrent connections
        limit_max_requests=10000,  # Increased requests before worker restart
        backlog=2048,  # Increased pending connections queue
        timeout_keep_alive=30,  # Reduce idle connection timeout
        access_log=True,  # Enable access logging
        log_level="info",  # Set log level to info for better debugging
        reload=DEBUG  # Enable auto-reload for development
    )
    server = uvicorn.Server(config)
    server.run()