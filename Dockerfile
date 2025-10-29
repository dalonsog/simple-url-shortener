# Build stage
FROM python:3.10 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Production stage
FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

WORKDIR /app

COPY ./urlshortener /app/urlshortener

ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "-m", "flask", "--app", "urlshortener/api", "run", "--debug"]
