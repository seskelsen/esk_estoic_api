@echo off
echo Inicializando o servidor da API de Citacoes Estoicas...
echo.

REM Muda para o diretorio do projeto
cd /d %~dp0

REM Ativa o ambiente virtual
call venv\Scripts\activate

echo.
echo Ambiente virtual ativado!
echo.
echo Iniciando o servidor uvicorn...
echo.
echo -------------------------------------------------
echo API de Citacoes Estoicas v1.5.0
echo -------------------------------------------------
echo * Rate limiting ativado: 60 requisicoes/minuto
echo * Cabeçalhos de seguranca configurados
echo * Servidor iniciando em modo de desenvolvimento
echo -------------------------------------------------
echo.
echo Acesse a aplicacao em http://localhost:8000
echo Documentacao em http://localhost:8000/docs

REM Para iniciar o servidor, execute:
REM python -m src.main
echo Pressione CTRL+C para encerrar o servidor
echo.

REM Inicia o servidor
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

REM Desativa o ambiente virtual quando o servidor for encerrado
call deactivate
