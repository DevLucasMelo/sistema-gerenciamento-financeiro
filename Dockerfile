# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Instala dependências de sistema necessárias para GTK, GObject e Pango
RUN apt-get update && apt-get install -y \
    libgirepository1.0-dev \
    libcairo2-dev \
    libglib2.0-dev \
    libpango1.0-dev \
    build-essential \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do projeto para o diretório de trabalho
COPY . /app/

# Instala as dependências a partir do requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Coleta os arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expõe a porta 8000 do contêiner
EXPOSE 8000

# Comando para iniciar o servidor Django com Gunicorn
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
