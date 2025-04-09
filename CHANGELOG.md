# Changelog

## [1.5.0] - 2025-04-08

### Adicionado

- Rate limiting para proteção contra abusos:
  - Limitador global: 60 requisições por minuto, 2 por segundo
  - Limites específicos por endpoint:
    - Citações diárias: 90 requisições por minuto
    - Citações aleatórias: 30 requisições por minuto
    - Lista completa de citações: 10 requisições por minuto
    - Busca por autor: 20 requisições por minuto
  - Respostas 429 (Too Many Requests) com cabeçalho Retry-After
  - Documentação atualizada com informações sobre limites

### Melhorado

- Descrições dos endpoints agora incluem informações sobre limites de taxa
- Configuração da API para mostrar informações detalhadas sobre rate limiting
- Robustez contra ataques de força bruta e DoS

## [1.4.0] - 2025-04-08

### Adicionado

- Tema escuro (dark mode) para a interface web com:
  - Alternância através de botão dedicado
  - Persistência da preferência do usuário via localStorage
  - Transições suaves entre temas
  - Esquema de cores otimizado para uso noturno
- Favicon personalizado com símbolo de coruja representando sabedoria
- Testes completos para componentes estáticos e middleware
- Documentação expandida sobre segurança e testes

### Melhorado

- Estrutura de testes organizada em três categorias:
  - Testes da API e endpoints
  - Testes de componentes estáticos
  - Testes de segurança e middleware
- Suporte adequado para CORS em todos os endpoints
- Handler global para requisições OPTIONS
- Tratamento adequado para solicitações de favicon

### Corrigido

- Erro 405 (Method Not Allowed) ao acessar favicon.ico
- Comportamento inconsistente do CORS em algumas rotas

## [1.3.1] - 2025-04-07

### Melhorado

- Implementação de cabeçalhos de segurança HTTP:
  - Content-Security-Policy (CSP) para controlar carregamento de recursos
  - X-Frame-Options para proteção contra clickjacking
  - X-Content-Type-Options para prevenir MIME-sniffing
- Conformidade com recomendações de segurança identificadas pelo ZAP Proxy

## [1.3.0] - 2025-04-07

### Adicionado

- Interface dinâmica com botões para citações aleatórias
- Alternância entre idiomas (português/inglês) na interface
- Funcionalidade de compartilhamento de citações
- Sistema de favoritos com armazenamento local
- Controles visuais para melhor experiência do usuário

### Melhorado

- Compatibilidade com acesso via IP, não apenas via localhost
- Robustez no carregamento de recursos estáticos com uso de URLs relativas
- Configuração CORS expandida para permitir acesso de qualquer origem
- Logs de depuração para facilitar resolução de problemas
- Documentação atualizada refletindo as novas funcionalidades

### Corrigido

- Problema de acesso à API quando usando endereço IP em vez de localhost
- Melhor manejo de erros nas requisições fetch
- Conflitos de caminho em ambientes de produção

## [1.2.0] - 2025-04-04

### Adicionado

- Documentação interativa da API usando Swagger/OpenAPI
- Interface ReDoc para documentação mais legível
- Modelos Pydantic para padronizar respostas da API
- Suporte para Docker com Dockerfile para containerização
- Arquivo Procfile para implantação no Heroku

### Melhorado

- Estrutura do código com uso de modelos de dados Pydantic
- Organização da API com tags para melhor navegação
- Descrições detalhadas de endpoints com exemplos
- Tratamento e documentação de erros da API
- Solução de conflitos de importação para melhor manutenção

## [1.1.0] - 2025-04-04

### Adicionado

- Interface web responsiva para exibição das citações
- Estrutura de arquivos CSS e JavaScript separados seguindo boas práticas
- Suporte para exibição da data atual na interface
- Aspas decorativas para melhorar a apresentação das citações

### Melhorado

- Refatoração do código para usar caminhos relativos em vez de caminhos absolutos
- Configuração do servidor usando variáveis de ambiente para facilitar implantação
- Ajuste da configuração CORS para permitir acesso de diferentes origens
- Separação do código em componentes (HTML, CSS e JavaScript) para melhor manutenção

### Corrigido

- Problema de CORS que impedia o carregamento das citações na interface web
- Caminhos hardcoded que dificultavam a implantação em diferentes ambientes

## [1.0.0] - 2024-03-26

### Adicionado

- Implementação inicial da API de citações estoicas
- Base de dados completa com citações para todos os 366 dias do ano
- Estrutura de arquivos organizada com separação de dados e lógica
- Sistema de cobertura para rastrear citações disponíveis

### Melhorado

- Remoção de citações duplicadas
- Organização cronológica das citações
- Documentação atualizada refletindo o estado atual do projeto

### Corrigido

- Padronização do formato das citações
- Consistência nas datas e formatação

## [0.2.0] - 2024-03-15

### Adicionado

- Citações para os meses de janeiro e fevereiro
- Citações para março (parcial)
- Sistema de rastreamento de cobertura de citações

## [0.1.0] - 2024-02-24

### Adicionado

- Estrutura inicial do projeto
- Configuração do ambiente de desenvolvimento
- Implementação básica da API
- Primeiras citações de teste
