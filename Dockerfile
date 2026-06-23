FROM python:3.11-slim

WORKDIR /app

COPY config/requirements-dev.txt ./config/requirements-dev.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r config/requirements-dev.txt

COPY src ./src
COPY projects ./projects
COPY config ./config

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

CMD ["python", "-m", "pytest", "src/shared/tests/", "-q"]
