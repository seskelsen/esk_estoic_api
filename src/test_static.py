import pytest
from fastapi.testclient import TestClient
from bs4 import BeautifulSoup
import os
from src.main import app, BASE_DIR
from unittest.mock import patch
from slowapi.errors import RateLimitExceeded

# Patch mais robusto para o rate limiter durante os testes
@pytest.fixture(autouse=True)
def patch_rate_limiter():
    # Patch para o decorador limiter.limit
    def fake_decorator(*args, **kwargs):
        def inner(func):
            return func
        return inner
    
    # Patch para o middleware SlowAPI para evitar que ele intercepte as requisições
    with patch('src.main.limiter.limit', side_effect=fake_decorator), \
         patch('src.main.SlowAPIMiddleware.dispatch', side_effect=lambda self, request, call_next: call_next(request)):
        # Também faz patch no exception handler para evitar respostas 429
        app.exception_handlers[RateLimitExceeded] = lambda req, exc: None
        yield

client = TestClient(app)

def test_index_html_served():
    """Testa se o arquivo index.html é servido corretamente quando a rota principal é acessada com Accept: text/html."""
    response = client.get("/", headers={"Accept": "text/html"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    # Verificar se o conteúdo contém elementos esperados
    soup = BeautifulSoup(response.content, 'html.parser')
    assert soup.title is not None
    assert "Citação Estoica do Dia" in soup.title.text
    
    # Verificar se os links para os arquivos CSS e JS estão corretos
    css_links = soup.find_all("link", rel="stylesheet")
    assert any("static/css/style.css" in link["href"] for link in css_links)
    
    js_scripts = soup.find_all("script")
    assert any("static/js/app.js" in script["src"] for script in js_scripts)

def test_css_file_served():
    """Testa se o arquivo CSS é servido corretamente."""
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]
    
    # Verificar se o conteúdo do arquivo corresponde ao arquivo real
    css_path = os.path.join(BASE_DIR, "static", "css", "style.css")
    with open(css_path, "rb") as f:
        expected_content = f.read()
    assert response.content == expected_content

def test_js_file_served():
    """Testa se o arquivo JavaScript é servido corretamente."""
    response = client.get("/static/js/app.js")
    assert response.status_code == 200
    assert "application/javascript" in response.headers["content-type"] or "text/javascript" in response.headers["content-type"]
    
    # Verificar se o conteúdo do arquivo corresponde ao arquivo real
    js_path = os.path.join(BASE_DIR, "static", "js", "app.js")
    with open(js_path, "rb") as f:
        expected_content = f.read()
    assert response.content == expected_content

def test_static_api_integration():
    """Testa a integração básica entre o frontend e a API verificando se o JavaScript pode fazer
    requisições para os endpoints da API e processar os resultados."""
    # Obter o arquivo JavaScript
    js_path = os.path.join(BASE_DIR, "static", "js", "app.js")
    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()
    
    # Verificar se o JS contém chamadas de API para os endpoints esperados
    assert "fetch(" in js_content
    
    # Verificar se os endpoints que o frontend provavelmente chama realmente existem e funcionam
    endpoints = [
        "/quote/today",
        "/quote/random",
        "/quote/today/en",
        "/quote/random/en"
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert "author" in data
        assert "date" in data
