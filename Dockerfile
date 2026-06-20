FROM python:3.11-slim

WORKDIR /app

# system dependencies (NO repo editing, NO sed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    aria2 \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# install python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

# run bot
CMD ["python", "main.py"]
