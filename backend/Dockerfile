FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD sh -c "echo 'Проверяем доступность базы...' && \
           until pg_isready -h postgres -U mapuser -p 5432 -d forestmap; do sleep 2; done && \
           echo 'База готова. Накатываем миграции...' && \
           alembic upgrade head && \
           echo 'Запускаем сервер...' && \
           exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"