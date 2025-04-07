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
echo Acesse a aplicacao em http://localhost:8000
echo Pressione CTRL+C para encerrar o servidor
echo.

REM Inicia o servidor
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

REM Desativa o ambiente virtual quando o servidor for encerrado
call deactivate
