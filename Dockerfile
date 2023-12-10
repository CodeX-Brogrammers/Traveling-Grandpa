FROM python:3.11.7-alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apk add --no-cache git
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt gunicorn


FROM python:3.11.7-alpine

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY nlu /app/nlu
COPY *.py .

RUN pip install --no-cache /wheels/*

ENV PYTHONPATH "${PYTHONPATH}:/app:/app/nlu"

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:3000", "--workers", "4", "--worker-class", "aiohttp.GunicornWebWorker"]