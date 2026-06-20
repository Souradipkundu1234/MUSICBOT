FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN sed -i '/yarnpkg/d' /etc/apt/sources.list || true

RUN apt-get update

RUN apt-get install -y ffmpeg git aria2

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
