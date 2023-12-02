FROM python:3.10.13-alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN apk add --no-cache git
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt gunicorn


FROM python:3.10.13-alpine

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY *.py .

RUN pip install --no-cache /wheels/*

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:3000", "--workers", "4", "--worker-class", "aiohttp.GunicornWebWorker"]