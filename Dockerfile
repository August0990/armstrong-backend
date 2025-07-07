FROM python:3.11

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary python-multipart aiofiles python-dotenv
RUN pip install --no-cache-dir fastapi==0.104.1 uvicorn==0.24.0 sqlalchemy==2.0.23 psycopg2==2.9.9 python-dotenv==1.0.0 python-multipart==0.0.6 django==4.2.7 gunicorn==21.2.0