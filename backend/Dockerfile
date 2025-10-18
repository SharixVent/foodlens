FROM python:3.11.10-slim-bookworm
ENV DEBIAN_FRONTEND=noninteractive PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN set -eux; apt-get update; apt-get install -y --no-install-recommends \
      tesseract-ocr tesseract-ocr-pol libmagic1 build-essential ca-certificates \
    ; rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
CMD ["bash","-lc","alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
