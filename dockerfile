FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
        git curl \
        libxml2-dev libxslt1-dev \
        python3-dev gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/user_files /app/jobs_data

ENV PORT=3000
EXPOSE 3000
ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]