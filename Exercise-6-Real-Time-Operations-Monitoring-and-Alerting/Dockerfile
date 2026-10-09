FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir prometheus-client==0.21.0

COPY delivery_metrics.py .

EXPOSE 8000

CMD ["python", "delivery_metrics.py"]
