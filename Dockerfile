FROM python:3.11-slim

WORKDIR /app

COPY . /app

# 🔥 Fix all apt issues + remove Yarn repo + install system packages
RUN rm -f /etc/apt/sources.list.d/yarn.list || true && \
    sed -i '/yarnpkg/d' /etc/apt/sources.list || true && \
    apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg git aria2 curl && \
    rm -rf /var/lib/apt/lists/*

# 🔥 Python setup
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 🚀 Run app
CMD ["python", "main.py"]
