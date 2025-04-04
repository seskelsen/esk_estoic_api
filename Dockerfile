FROM python:3.9-slim

WORKDIR /app

# Copiar arquivos de requisitos e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte
COPY . .

# Variáveis de ambiente
ENV APP_ENV=production
ENV PORT=8000
ENV HOST=0.0.0.0
ENV ALLOWED_ORIGINS=*

# Expor a porta
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["python", "-m", "src.main"]