# API de Citações Estoicas

## Descrição

Este projeto é uma API que fornece citações estoicas para cada dia do ano, com suporte para português e inglês. Além da API, o projeto inclui uma interface web responsiva e dinâmica para visualização das citações diárias e interação do usuário.

## Funcionalidades

- API RESTful para acesso a citações estoicas
- Interface web responsiva para visualização das citações
- Interface dinâmica com botões de interação:
  - Citações aleatórias com um clique
  - Alternância entre português e inglês
  - Sistema de favoritos com armazenamento local
  - Compartilhamento de citações
- Documentação interativa com Swagger e ReDoc
- Suporte para português e inglês
- Citações específicas para cada dia do ano
- Citações aleatórias
- Design moderno e compatível com dispositivos móveis
- Suporte para Docker e implantação em nuvem
- Compatibilidade de acesso via IP ou domínio, não apenas localhost

## Instalação

### Pré-requisitos

- Python 3.9+
- pip (gerenciador de pacotes Python)

### Instalação local

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/esk_estoic_api.git
   cd esk_estoic_api
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o servidor:

   ```bash
   # Usando os scripts de inicialização automatizados:
   
   # No Windows - execute o arquivo:
   start_server.bat
   
   # No Linux/macOS - execute o arquivo (dê permissão primeiro):
   chmod +x start_server.sh
   ./start_server.sh
   
   # OU manualmente:
   python -m src.main
   ```

5. Acesse a aplicação:
   - API: <http://localhost:8000/quote/today>
   - Interface web: <http://localhost:8000>

## Uso da API

A API está disponível em `http://localhost:8000`. Aqui estão os endpoints disponíveis:

### Documentação Interativa

```
GET /docs
```

Acesse a documentação interativa Swagger para testar todos os endpoints diretamente no navegador.

```
GET /redoc
```

Visualize a documentação completa da API em um formato mais legível com ReDoc.

### Citação do dia

```
GET /quote/today
```

Retorna a citação correspondente ao dia atual.

### Citação do dia em inglês

```
GET /quote/today/en
```

Retorna a citação do dia atual em inglês.

### Citação aleatória

```
GET /quote/random
```

Retorna uma citação aleatória.

### Citação aleatória em inglês

```
GET /quote/random/en
```

Retorna uma citação aleatória em inglês.

### Todas as citações

```
GET /quotes
```

Retorna todas as citações disponíveis.

### Citações por autor

```
GET /quotes/{author}
```

Retorna todas as citações de um autor específico.

## Configuração para produção

O projeto suporta configuração via variáveis de ambiente:

- `APP_ENV`: Define o ambiente ("development" ou "production")
- `PORT`: Define a porta do servidor (padrão: 8000)
- `HOST`: Define o host do servidor (padrão: "0.0.0.0")
- `ALLOWED_ORIGINS`: Define as origens permitidas para CORS (separadas por vírgula)

Exemplo de configuração para produção:

```bash
export APP_ENV=production
export PORT=8080
export ALLOWED_ORIGINS=https://seu-site.com,https://outro-site.com
python -m src.main
```

## Estrutura do projeto

```
esk_estoic_api/
├── index.html              # Interface web principal
├── requirements.txt        # Dependências do projeto
├── CHANGELOG.md            # Registro de alterações
├── README.md               # Documentação
├── TODO.md                 # Lista de tarefas pendentes
├── Dockerfile              # Configuração para containerização
├── Procfile                # Configuração para deploy no Heroku
├── start_server.bat        # Script para iniciar o servidor no Windows
├── start_server.sh         # Script para iniciar o servidor no Linux/macOS
├── src/                    # Código-fonte da API
│   ├── main.py             # Arquivo principal da API
│   ├── test_main.py        # Testes da API
│   └── data/               # Dados da aplicação
│       └── quotes.py       # Banco de dados de citações
└── static/                 # Arquivos estáticos
    ├── css/                # Estilos CSS
    │   └── style.css       # Estilos da interface web
    └── js/                 # JavaScript
        └── app.js          # Lógica da interface web
```

## Implantação

### Docker

O projeto inclui um Dockerfile para facilitar a containerização:

```bash
# Construir a imagem
docker build -t estoic-api .

# Executar o container
docker run -p 8000:8000 -e APP_ENV=production estoic-api
```

### Heroku

Para implantar no Heroku, utilize o Procfile incluído:

```bash
# Login no Heroku
heroku login

# Criar um novo app
heroku create sua-app-estoica

# Fazer deploy
git push heroku main
```

## Documentação da API

A API oferece documentação interativa que pode ser acessada de duas formas:

1. **Swagger UI** (`/docs`): Interface interativa que permite:
   - Visualizar todos os endpoints disponíveis
   - Testar chamadas API diretamente no navegador
   - Ver modelos de dados e exemplos de respostas
   - Entender códigos de erro possíveis

2. **ReDoc** (`/redoc`): Documentação mais legível com:
   - Detalhes completos sobre cada endpoint
   - Exemplos de uso e respostas
   - Organização por tags e categorias

A documentação inclui exemplos, modelos de dados e explicações detalhadas para facilitar a integração com outros sistemas.

## Contribuição

Contribuições são bem-vindas! Por favor, consulte o arquivo TODO.md para ver as tarefas pendentes e siga estas etapas:

1. Faça um fork do repositório
2. Crie um branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para o branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
