import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import patch, MagicMock
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
    def fake_call_next(request):
        async def mock_call_next(request):
            # Ignora a verificação de rate limit
            return await app.middleware_stack.middlewares[0].dispatch_func(request)
        return mock_call_next
    
    with patch('src.main.limiter.limit', side_effect=fake_decorator), \
         patch('src.main.SlowAPIMiddleware.dispatch', side_effect=lambda self, request, call_next: call_next(request)):
        # Também faz patch no exception handler para evitar respostas 429
        app.exception_handlers[RateLimitExceeded] = lambda req, exc: None
        yield

# Cria um cliente de teste com o rate limiting desativado
client = TestClient(app)

def test_security_headers_middleware():
    """Testa se os cabeçalhos de segurança estão sendo adicionados corretamente pelo middleware."""
    response = client.get("/")
    
    # Verificar a presença e o valor correto dos cabeçalhos de segurança
    assert "content-security-policy" in response.headers
    assert "default-src 'self'; script-src 'self'; style-src 'self';" in response.headers["content-security-policy"]
    
    assert "x-frame-options" in response.headers
    assert response.headers["x-frame-options"] == "DENY"
    
    assert "x-content-type-options" in response.headers
    assert response.headers["x-content-type-options"] == "nosniff"

def test_security_headers_on_json_endpoint():
    """Testa se os cabeçalhos de segurança estão sendo adicionados nas respostas JSON."""
    response = client.get("/quote/today")
    
    # Verificar a presença e o valor correto dos cabeçalhos de segurança
    assert "content-security-policy" in response.headers
    assert "default-src 'self'; script-src 'self'; style-src 'self';" in response.headers["content-security-policy"]
    
    assert "x-frame-options" in response.headers
    assert response.headers["x-frame-options"] == "DENY"
    
    assert "x-content-type-options" in response.headers
    assert response.headers["x-content-type-options"] == "nosniff"

def test_security_headers_on_static_files():
    """Testa se os cabeçalhos de segurança estão sendo adicionados nas respostas de arquivos estáticos."""
    response = client.get("/static/css/style.css")
    
    # Verificar a presença e o valor correto dos cabeçalhos de segurança
    assert "content-security-policy" in response.headers
    assert "default-src 'self'; script-src 'self'; style-src 'self';" in response.headers["content-security-policy"]
    
    assert "x-frame-options" in response.headers
    assert response.headers["x-frame-options"] == "DENY"
    
    assert "x-content-type-options" in response.headers
    assert response.headers["x-content-type-options"] == "nosniff"

def test_cors_headers_on_preflight():
    """Testa se os cabeçalhos CORS estão sendo adicionados nas respostas de preflight OPTIONS."""
    response = client.options("/quote/today", headers={"Origin": "http://localhost:3000"})
    
    # Verificar a presença e o valor correto dos cabeçalhos CORS
    assert "access-control-allow-origin" in response.headers
    assert "*" in response.headers["access-control-allow-origin"]
    
    assert "access-control-allow-methods" in response.headers
    assert "GET" in response.headers["access-control-allow-methods"]
    assert "OPTIONS" in response.headers["access-control-allow-methods"]
    
    assert "access-control-allow-headers" in response.headers
    assert "*" in response.headers["access-control-allow-headers"]
    
    assert "access-control-max-age" in response.headers
    assert response.headers["access-control-max-age"] == "3600"

def test_cors_headers_on_regular_response():
    """Testa se os cabeçalhos CORS estão sendo adicionados nas respostas regulares quando uma origem é especificada."""
    response = client.get("/quote/today", headers={"Origin": "http://localhost:3000"})
    
    # Verificar a presença e o valor correto dos cabeçalhos CORS
    assert "access-control-allow-origin" in response.headers
    assert "*" in response.headers["access-control-allow-origin"]
