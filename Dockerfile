FROM python:3.11-slim

WORKDIR /app

# system packages install (NO repo edit needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    aria2 \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# requirements install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

CMD ["python", "main.py"]
