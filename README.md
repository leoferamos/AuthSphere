# AuthSphere

**Sistema Centralizado de Autenticação e Administração de Usuários**

<p align="center">
  <img src="assets/logo.png" alt="Logo AuthSphere" width="700"/>
</p>

## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Arquitetura](#arquitetura)
- [Como Executar](#como-executar)
- [Configuração de Campos Dinâmicos](#configuração-de-campos-dinâmicos)
- [Segurança e Boas Práticas](#segurança-e-boas-práticas)
- [Referências](#referências)

---

## Sobre o Projeto

O **AuthSphere** é uma solução centralizada de autenticação e administração de usuários, desenvolvida para facilitar a integração com outros sistemas, garantir segurança, conformidade com a LGPD e proporcionar flexibilidade para diferentes cenários de uso.

---

## Funcionalidades

- Cadastro de usuários
- Login seguro (OAuth2/JWT)
- Controle de permissões baseado em papéis (RBAC)
- Reset de senha seguro
- Registro de logs de acesso e alterações
- Exclusão e anonimização de conta conforme LGPD
- Interface administrativa (frontend próprio e seguro)
- Integração via API REST com qualquer sistema
- Configuração dinâmica de campos do formulário de cadastro/login

---

## Requisitos

### Requisitos Funcionais

- Cadastro e login de usuários
- Reset de senha
- Controle de acesso por papéis e permissões (RBAC)
- Registro e consulta de logs
- Painel administrativo para gestão de usuários e permissões
- Integração via API REST documentada

### Requisitos Não Funcionais

- Segurança: hash de senhas, proteção contra ataques, uso de HTTPS, tokens JWT
- Modularidade: backend e frontend desacoplados
- Escalabilidade: serviços separados para frontend, backend e banco de dados
- Documentação: OpenAPI/Swagger, guia de integração
- Conformidade LGPD: consentimento, anonimização, logs de acesso e exclusão de dados
- Facilidade de customização do frontend

---

## Arquitetura

- **Frontend**: React (ou Vue), desacoplado, personalizável, configurável via variáveis de ambiente.
- **Backend**: Python (FastAPI), seguindo boas práticas de Clean Architecture, com endpoints REST para autenticação, RBAC, logs, etc.
- **Banco de Dados**: SQL (MySQL), armazena usuários, papéis, permissões, logs e dados sensíveis.
- **Integração**: API REST documentada (Swagger/OpenAPI), fácil de consumir por qualquer sistema (Go, Python, JavaScript, etc.).

### Fluxo de Autenticação

1. Usuário acessa o frontend de login.
2. Após login, recebe um token JWT.
3. Frontend redireciona o usuário para o sistema integrado, enviando o token.
4. O backend do sistema integrado valida o token em todas as requisições.
5. Operações sensíveis são sempre validadas no backend.

---

## Como Executar

### Pré-requisitos

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- Git

### Passos

1. **Clone o repositório**
    ```
    git clone https://github.com/leoferamos/AuthSphere.git
    cd AuthSphere
    ```

2. **Configure as variáveis de ambiente**
    - Copie e edite os arquivos `.env.example` e `.env.db.example` para `.env` e `.env.db`, respectivamente.

3. **Suba os serviços**
    ```
    docker-compose up --build
    ```

4. **Rode as migrações do banco**
    ```
    docker-compose exec backend alembic upgrade head
    ```

5. **Acesse os sistemas**
    - **Backend (API/Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
    - **Frontend:** [http://localhost:5173](http://localhost:5173)

---

## Configuração de Campos Dinâmicos

O painel administrativo permite ativar ou desativar campos do formulário de cadastro e login, conforme a necessidade do negócio. Os campos disponíveis são:

- E-mail
- Senha
- Nome de usuário
- Nome
- Sobrenome
- Telefone
- Data de nascimento

> **Observação:** Não é permitido criar campos totalmente livres, garantindo integridade e validação consistente.

---

## Segurança e Boas Práticas

- Tokens JWT assinados e validados a cada requisição
- RBAC com papéis e permissões definidos
- Logs de acesso e alterações, acessíveis apenas por admins
- Painel administrativo protegido por RBAC e autenticação forte
- Variáveis sensíveis nunca expostas no frontend
- Consentimento e anonimização conforme LGPD
- Toda validação e autorização feita no backend


## Referências

- LGPD - Lei Geral de Proteção de Dados (Lei nº 13.709/2018)
- ISO/IEC 27001:2013
- [AuthSphere – Documentação do Projeto](https://github.com/leoferamos/AuthSphere)
- PRESSMAN, R. S. Engenharia de Software. 7. ed. São Paulo: McGraw-Hill, 2011.

---

Se precisar de instruções para deploy em produção, exemplos de integração ou dúvidas sobre uso, consulte a documentação ou abra uma issue!
