# Serviço de E-mails Wiplay

Serviço FastAPI para envio de e-mails através de templates HTML e fila Kafka.

---

## Execução Local (Desenvolvimento)

### Pré-requisitos

- Python 3.12 ou superior
- Ambiente virtual Python (venv)

### 1. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual (se ainda não existe)
python -m venv env

# Ativar ambiente virtual
# Windows PowerShell:
.\env\Scripts\Activate.ps1

# Windows CMD:
.\env\Scripts\activate.bat

# Linux/Mac:
source env/bin/activate
```

### 2. Instalar Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar Credenciais

Crie o arquivo `config.cfg` na raiz do projeto:

```ini
[DEFAULT]
AUTH_TOKEN=seu_token_aqui
EMAIL_WIPLAY_TOPICO=nome_do_topico_kafka
SERVER_IP=10.1.2.224:9092
PORT=8500
LOG_LEVEL=info
```

> A aplicação também suporta arquivo `.env` ou variáveis de ambiente. Prioridade: Variáveis de ambiente > .env > config.cfg

### 4. Executar a Aplicação

```bash
python -m app.main
# ou
python app/main.py
```

A aplicação estará disponível em: `http://localhost:8500`

- Documentação Swagger: `http://localhost:8500/docs`
- Documentação ReDoc: `http://localhost:8500/redoc`

---

## Deploy Docker

### 1. Pré-requisitos

Certifique-se de ter:

- Docker instalado
- Acesso à internet para baixar imagens e dependências
- Credenciais do Docker Hub:

```
URL: https://hub.docker.com/
Usuário: dev@wiplay.com.br
Senha: B4n$#!987
```

---

### 2. Login no Docker Hub

Faça login para poder enviar ou atualizar imagens:

```bash
docker login -u dev@wiplay.com.br
```

---

### 3. Dockerfile recomendado

O `Dockerfile` do projeto:

```dockerfile
# Imagem base Python
FROM python:3.12-slim

# Atualiza pacotes do sistema
RUN apt-get update && apt-get upgrade -y

# Instala dependências Python
RUN pip install --upgrade pip

# Define diretório de trabalho
WORKDIR /app

# Copia o código da aplicação
COPY . /app

# Instala dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da aplicação
EXPOSE 8500

# Comando para iniciar a aplicação
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8500", "--timeout", "300"]
```

> Ajuste `app.main:app` para o caminho do arquivo principal da sua aplicação.

---

### 4. Build da imagem Docker

```bash
docker build -t dockerwip624/emails:v2.0 .
```

- `-t` define a tag da imagem (`v2.0`).
- `.` indica o diretório atual como contexto do build.

---

### 5. Executando o container

**Opção A: Usando arquivo config.cfg (incluído na imagem)**

```bash
docker run -d -p 8500:8500 --name emails dockerwip624/emails:v2.0
```

**Opção B: Usando variáveis de ambiente**

```bash
docker run -d -p 8500:8500 --name emails \
  -e AUTH_TOKEN=seu_token_aqui \
  -e EMAIL_WIPLAY_TOPICO=nome_do_topico_kafka \
  -e SERVER_IP=10.1.2.224:9092 \
  -e PORT=8500 \
  -e LOG_LEVEL=info \
  dockerwip624/emails:v2.0
```

**Parâmetros:**
- `-d`: executa em background.
- `-p 8500:8500`: mapeia a porta 8500.
- `--name emails`: nome do container.
- `-e`: define variáveis de ambiente individuais.

---

### 6. Verificando containers ativos

```bash
docker container ls
# ou
docker ps
```

---

### 7. Atualizando o container

1. Pare o container atual:

```bash
docker container stop emails
```

2. Remova o container antigo:

```bash
docker container rm emails
```

3. Build da nova versão:

```bash
docker build -t dockerwip624/emails:v2.0 .
```

4. Execute o container atualizado:

```bash
docker run -d -p 8500:8500 --name emails dockerwip624/emails:v2.0
```

Alternativamente, usando pull no servidor:

```bash
docker pull dockerwip624/emails:v2.0
docker run -d -p 8500:8500 --name emails dockerwip624/emails:v2.0
```

---

### 8. Publicando no Docker Hub

```bash
docker push dockerwip624/emails:v2.0
```

> Lembre-se de estar logado no Docker Hub antes do push.

---

### 9. Resolução de Conflitos

Se houver conflitos com containers existentes:

```bash
# Parar e remover container existente
docker stop emails
docker rm emails

# Executar novo container
docker run -d -p 8500:8500 --name emails dockerwip624/emails:v2.0
```

---

## Endpoints da API

A aplicação expõe os seguintes endpoints:

- `POST /email/wiplay/convite` - Envio de e-mail de convite
- `POST /email/wiplay/change_phone` - E-mail de confirmação de troca de telefone
- `POST /email/wiplay/erro_login` - E-mail de erro de login
- `POST /email/wiplay/recuperar_senha` - E-mail de recuperação de senha
- `POST /email/wiplay/login_bloqueado` - E-mail de login bloqueado
- `POST /email/wiplay/navegador_desconhecido` - E-mail de navegador desconhecido
- `POST /email/wiplay/verificacao_email` - E-mail de verificação

Todos os endpoints requerem autenticação via Bearer Token no header `Authorization`.

### Endpoints de Health Check

- `GET /health` - Status básico da aplicação
- `GET /health/kafka` - Status detalhado da conexão com Kafka

Os endpoints de health check **não requerem autenticação**.

---

## Estrutura do Projeto

```
emails/
├── app/                    # Aplicação principal
│   ├── main.py           # Arquivo principal da aplicação
│   ├── core/              # Configuração e exceções
│   │   ├── config.py     # Configurações e variáveis de ambiente
│   │   └── exceptions.py # Exceções customizadas
│   ├── models/            # Modelos de dados
│   │   ├── email.py      # Modelo de e-mail
│   │   └── types.py      # Tipos e enums
│   ├── services/          # Serviços de negócio
│   │   ├── email_service.py # Serviço de e-mail
│   │   └── kafka.py       # Serviço Kafka
│   ├── utils/             # Utilitários
│   │   └── templates.py   # Handler de templates HTML
│   ├── middleware/        # Autenticação
│   │   └── auth.py        # Validação de token
│   └── api/               # Rotas da API
│       ├── routes.py      # Rotas de e-mail
│       └── health.py      # Health checks
├── html_messages/         # Templates HTML de e-mail
├── Dockerfile             # Configuração Docker
├── requirements.txt       # Dependências Python
├── config.cfg             # Configurações (não versionado)
└── README.md             # Este arquivo
```

---

## Notas Técnicas

- A aplicação usa porta 8500 por padrão
- Utiliza Gunicorn com Uvicorn Worker em produção
- Mensagens são enviadas via Kafka para processamento assíncrono
- Templates HTML estão em `html_messages/`

---

## Troubleshooting

### Erro ao executar localmente

- Verifique se o ambiente virtual está ativado
- Confirme que todas as dependências estão instaladas: `pip install -r requirements.txt`
- Verifique se o arquivo `config.cfg` existe na raiz do projeto e está configurado corretamente
- Confirme que todas as variáveis obrigatórias estão presentes: `AUTH_TOKEN`, `EMAIL_WIPLAY_TOPICO`, `SERVER_IP`

### Erro de conexão com Kafka

- Verifique se o serviço Kafka está rodando
- Confirme as configurações de conexão no arquivo `config.cfg`

### Container não inicia

- Verifique os logs: `docker logs emails`
- Confirme se a porta 8500 não está em uso: `netstat -an | findstr 8500` (Windows) ou `lsof -i :8500` (Linux/Mac)
- Verifique se as variáveis de ambiente foram passadas corretamente (`-e`) ou se o arquivo `config.cfg` está incluído na imagem
