# Imagem base Python
FROM python:3.12-slim

# Atualiza pacotes do sistema
RUN apt-get update && apt-get upgrade -y

# Define diretório de trabalho
WORKDIR /app

# Copia o código da aplicação
COPY . /app

# Instala dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt


# Exponha a porta que será utilizada
EXPOSE 8500

# Defina o comando padrão para rodar a aplicação
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8500", "--timeout", "300"]


# docker estação de trabalho
#-------------------------------------------------------------
# docker build -t dockerwip624/emails:v2.0 .
# docker push dockerwip624/emails:v2.0
# docker run -d -p 8500:8500 --name emails dockerwip624/emails:v2.0


# Servidor
# ------------------------------------------------------------------------------------
# docker container ls
# docker container stop <numero>
# docker container rm <numero>
# docker pull dockerwip624/emails:v2.0
# docker run -d -p 8500:8500 --name emails dockerwip624/emails:v2.0


# Conflitos
# ------------------------------------------------------------------------------------
# docker stop emails
# docker rm emails