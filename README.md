# Pharmacy Management Django API

Este projeto é uma API de gerenciamento de farmácia construída com Django e PostgreSQL, usando Docker para facilitar a configuração.

## Tecnologias
- Django 3.2
- PostgreSQL
- Docker e Docker Compose
- Django Rest Framework (DRF)
- SimpleJWT para autenticação
- drf-yasg para documentação

## Estrutura do Projeto
- **pharmacy_management_django_api**: Contém configurações do Django (settings, urls, wsgi, etc.).
- **pharmacy_management_app**: Principal app da aplicação, com modelos, views, rotas e regras de negócio.
  - **models**: Define as classes que representam dados, como User, Product e BankAccount.
  - **views**: Implementa funcionalidades para manipular dados e enviar respostas (Controllers).
  - **routes**: Configura URLs e roteamento via DRF.
  - **management/commands**: Scripts de inicialização, como o comando de seed (popula o banco).
- **docker-compose.yml**: Configura os containers (db, adminer e api_web).
- **manage.py**: Ponto de entrada para executar comandos Django (migrações, server, etc.).

## Uso do SOLID
Cada classe tem responsabilidade única (SRP) e as dependências são injetadas ou resolvidas usando recursos nativos do Django, mantendo o projeto modular e organizado.

## Como Rodar
1. Instale o Docker e o Docker Compose.
2. Ajuste o arquivo `.env` se necessário (banco de dados, credenciais, etc.).
3. Na raiz do projeto, execute:
   ```bash
   docker-compose up --build
   ```
4. A API estará em <http://localhost:8000>, e o Adminer em <http://localhost:8080>.
5. O Swagger estará em <http://localhost:8000/swagger>.
6. Por padrão o user é o especificado no, sendo o desse projeto: "admin@example.com" e "adminpassword"

Para parar, use:
```bash
docker-compose down
```