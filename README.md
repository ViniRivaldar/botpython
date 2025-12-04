# Audit Logs API

API REST para consulta de logs de auditoria coletados por middleware em aplicações.

## 📋 Sobre o Projeto

Este projeto fornece uma API HTTP que expõe logs de auditoria armazenados em um banco de dados PostgreSQL. Os logs são coletados através de um middleware instalado em outras aplicações, que captura informações detalhadas de requisições, respostas e possíveis ameaças de segurança.

## 🚀 Funcionalidades

- **Consulta de logs** com paginação
- **Busca incremental** usando `since_id` para sincronização
- **Limite configurável** de registros por requisição
- **Pool de conexões** otimizado com asyncpg
- **Health check** para monitoramento

## 🏗️ Arquitetura

```
┌─────────────────┐
│   Aplicação     │
│   com Middleware│──┐
└─────────────────┘  │
                     │ Captura logs
┌─────────────────┐  │
│   PostgreSQL    │◄─┘
│   (audit_logs)  │
└────────┬────────┘
         │
         │ Consulta
         │
┌────────▼────────┐
│  Audit Logs API │
│   (FastAPI)     │
└─────────────────┘
```

## 📦 Instalação

### Pré-requisitos

- Python 3.10+
- PostgreSQL com tabela `audit_logs`
- pip ou poetry

### Passos

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd botpython
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
```

## 🎯 Uso

### Iniciar o servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints

#### Health Check
```http
GET /health
```

**Resposta:**
```json
{
  "status": "ok"
}
```

#### Consultar Logs
```http
GET /audit_logs?limit=100&since_id=1000
```

**Parâmetros:**
- `limit` (opcional): Número máximo de registros (1-5000, padrão: 100)
- `since_id` (opcional): Retorna apenas logs com ID maior que o especificado

**Resposta:**
```json
[
  {
    "id": 1001,
    "timestamp": "2024-12-04T10:30:00",
    "action": "login",
    "status": 200,
    "email": "user@example.com",
    "ip": "192.168.1.1",
    "user_agent": "Mozilla/5.0...",
    "method": "POST",
    "response_time": 150.5,
    "threats": null,
    "user_exists": true
  }
]
```

### Exemplos de uso

**Buscar os últimos 50 logs:**
```bash
curl "http://localhost:8000/audit_logs?limit=50"
```

**Buscar logs incrementalmente (sincronização):**
```bash
# Primeira requisição
curl "http://localhost:8000/audit_logs?limit=100"

# Próximas requisições usando o último ID recebido
curl "http://localhost:8000/audit_logs?since_id=1234&limit=100"
```

## 📊 Estrutura da Tabela audit_logs

A tabela `audit_logs` deve conter as seguintes colunas:

- `id`: Identificador único (serial/bigserial)
- `timestamp`: Data/hora do evento
- `action`: Ação realizada (login, register, etc.)
- `status`: Código HTTP da resposta
- `email`: Email do usuário (se aplicável)
- `email_raw`: Email não processado
- `ip`: Endereço IP de origem
- `user_agent`: User agent do navegador/cliente
- `headers`: Cabeçalhos HTTP (JSONB)
- `request_body`: Corpo da requisição (JSONB)
- `threats`: Ameaças detectadas (JSONB)
- `reason`: Motivo de bloqueio/alerta
- `user_id`: ID do usuário
- `response_time`: Tempo de resposta em ms
- `db_query_time`: Tempo de query no banco
- `request_size`: Tamanho da requisição
- `method`: Método HTTP (GET, POST, etc.)
- `protocol`: Protocolo usado
- `user_exists`: Se o usuário existe no sistema
- `error_message`: Mensagem de erro
- `error_stack`: Stack trace de erros

## 🛠️ Tecnologias

- **FastAPI**: Framework web moderno e rápido
- **asyncpg**: Driver PostgreSQL assíncrono de alta performance
- **uvicorn**: Servidor ASGI
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 📁 Estrutura do Projeto

```
botpython/
├── .gitignore
├── README.md
├── requirements.txt
├── .env.example
├── main.py          # Endpoints da API
└── db.py            # Funções de acesso ao banco
```

## 🔒 Segurança

- Configure `DATABASE_URL` com credenciais seguras
- Use SSL para conexão com PostgreSQL em produção
- Considere adicionar autenticação/autorização nos endpoints
- Implemente rate limiting para prevenir abuso

## 🚀 Deploy

### Produção com Docker (recomendado)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Variáveis de ambiente em produção

```env
DATABASE_URL=postgresql://user:pass@db-host:5432/dbname?ssl=require
```

## 📝 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

---

Desenvolvido com ❤️ usando FastAPI
