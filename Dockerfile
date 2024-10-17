FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgirepository1.0-dev \
    libcairo2-dev \
    libglib2.0-dev \
    libpango1.0-dev \
    build-essential \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
