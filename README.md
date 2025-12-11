# Serviço de E-mails Wiplay

Serviço FastAPI para envio de e-mails através de templates HTML e fila Kafka.

## Sobre o arquivo __init__.py

O arquivo `__init__.py` está vazio e não executa nenhuma ação automaticamente quando o terminal é aberto. Sua função é marcar o diretório como um pacote Python, permitindo que outros módulos importem código deste diretório.

Se alguma ação ocorre automaticamente ao abrir o terminal, pode ser devido a:
- Ativação automática do ambiente virtual (se configurado no shell)
- Scripts de inicialização do sistema operacional
- Configurações do terminal ou IDE

---

## Execução Local (Desenvolvimento)

### Pré-requisitos

- Python 3.12 ou superior
- Ambiente virtual Python (venv)
- Credenciais configuradas em `env/credentials.cfg`

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

Crie o arquivo `env/credentials.cfg` com as seguintes variáveis:

```cfg
AUTH_TOKEN=seu_token_aqui
EMAIL_WIPLAY_TOPICO=nome_do_topico_kafka
```

### 4. Executar a Aplicação

```bash
python main.py
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

### 3. Build da Imagem Docker

```bash
docker build -t dockerwip624/emails:v1.41 .
```

- `-t` define a tag da imagem (`v1.41`)
- `.` indica o diretório atual como contexto do build

---

### 4. Executando o Container

```bash
docker run -d -p 8500:8500 --name emails dockerwip624/emails:v1.41
```

- `-d`: executa em background
- `-p 8500:8500`: mapeia a porta 8500 do host para a porta 8500 do container
- `--name emails`: nome do container

---

### 5. Verificando Containers Ativos

```bash
docker container ls
# ou
docker ps
```

---

### 6. Ver Logs do Container

```bash
docker logs emails
# ou para seguir os logs em tempo real:
docker logs -f emails
```

---

### 7. Atualizando o Container

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
docker build -t dockerwip624/emails:v1.41 .
```

4. Execute o container atualizado:

```bash
docker run -d -p 8500:8500 --name emails dockerwip624/emails:v1.41
```

Alternativamente, usando pull no servidor:

```bash
docker pull dockerwip624/emails:v1.41
docker run -d -p 8500:8500 --name emails dockerwip624/emails:v1.41
```

---

### 8. Publicando no Docker Hub

```bash
docker push dockerwip624/emails:v1.41
```

Nota: Lembre-se de estar logado no Docker Hub antes do push.

---

### 9. Resolução de Conflitos

Se houver conflitos com containers existentes:

```bash
# Parar e remover container existente
docker stop emails
docker rm emails

# Executar novo container
docker run -d -p 8500:8500 --name emails dockerwip624/emails:v1.41
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

---

## Estrutura do Projeto

```
emails/
├── env/                    # Credenciais (não versionado)
│   └── credentials.cfg
├── html_messages/          # Templates HTML de e-mail
├── routes/
│   ├── controllers/        # Lógica de negócio
│   ├── helpers/           # Funções auxiliares
│   ├── models/            # Modelos de dados
│   ├── security/          # Validação de tokens
│   └── views/             # Rotas da API
├── main.py                # Arquivo principal da aplicação
├── Dockerfile             # Configuração Docker
├── requirements.txt       # Dependências Python
└── README.md             # Este arquivo
```

---

## Segurança

- Todas as rotas requerem autenticação via Bearer Token
- Credenciais devem estar em `env/credentials.cfg` (não versionado)
- Token configurado via variável `AUTH_TOKEN` no arquivo de credenciais

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
- Verifique se o arquivo `env/credentials.cfg` existe e está configurado corretamente

### Erro de conexão com Kafka

- Verifique se o serviço Kafka está rodando
- Confirme as configurações de conexão no código

### Container não inicia

- Verifique os logs: `docker logs emails`
- Confirme se a porta 8500 não está em uso: `netstat -an | findstr 8500` (Windows) ou `lsof -i :8500` (Linux/Mac)

