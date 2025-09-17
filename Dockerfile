FROM python:3.12-slim
LABEL authors="Kelvyn"

WORKDIR /app

# Instala netcat (necessário para wait-for-it.sh)
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# Copia o script wait-for-it.sh para dentro da imagem
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

#CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
# Usa o wait-for-it para garantir que o banco está pronto antes de subir o gunicorn
CMD ["/wait-for-it.sh", "database", "5432", "--", "gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
#FROM python:3.12-slim
#LABEL authors="Kelvyn"
#
#WORKDIR /app
#
## Instala dependências de sistema (netcat para wait-for-it)
#RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
#
## Instala requirements
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#
## Copia todo o projeto
#COPY . .
#
## Copia wait-for-it para o PATH
#COPY wait-for-it.sh /usr/local/bin/wait-for-it
#RUN chmod +x /usr/local/bin/wait-for-it
#
#ENV FLASK_APP=wsgi.py
#ENV FLASK_ENV=production
#
## Usa wait-for-it para esperar o banco antes de subir a API
#CMD ["wait-for-it", "database:5432", "--", "gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
