# Use uma imagem do Python como base
FROM python:3.12-slim

# Defina o diretório de trabalho para a pasta 'app'
WORKDIR /emails

# Copie o arquivo requirements.txt para o container
COPY . .

# Instale as dependências a partir do requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade

RUN pip install --upgrade pip

RUN pip install six
RUN pip install kafka-python
RUN pip install python-multipart
RUN pip install confluent-kafka
RUN pip install gunicorn==23.0.0

RUN pip install --no-cache-dir -r requirements.txt


# Exponha a porta que será utilizada
EXPOSE 8500

# Defina o comando padrão para rodar a aplicação
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8500","--timeout","300"]


# docker estação de trabalho
#-------------------------------------------------------------
# docker build -t dockerwip624/emails:v1.41 .
# docker push dockerwip624/emails:v1.41
# docker run -d -p 8500:8500 --name emails dockerwip624/emails:v1.41


# Servidor
# ------------------------------------------------------------------------------------
# docker container ls
# docker container stop <numero>
# docker container rm <numero>
# docker pull dockerwip624/emails:v1.41
# docker run -d -p 8500:8500 --name emails dockerwip624/emails:v1.41


# Conflitos
# ------------------------------------------------------------------------------------
# docker stop emails
# docker rm emails