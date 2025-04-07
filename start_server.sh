#!/bin/bash
echo "Inicializando o servidor da API de Citacoes Estoicas..."
echo

# Muda para o diretório do projeto (onde este script está localizado)
cd "$(dirname "$0")"

# Ativa o ambiente virtual
source venv/bin/activate

echo
echo "Ambiente virtual ativado!"
echo
echo "Iniciando o servidor uvicorn..."
echo
echo "Acesse a aplicacao em http://localhost:8000"
echo "Pressione CTRL+C para encerrar o servidor"
echo

# Inicia o servidor
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Desativa o ambiente virtual quando o servidor for encerrado
deactivate
