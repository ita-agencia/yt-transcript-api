# Dockerfile

FROM python:3.11-slim

# Instala ffmpeg (necessário para yt-dlp lidar com legendas) e curl
RUN apt-get update && apt-get install -y ffmpeg curl && \
    pip install --upgrade pip

# Copia o requirements.txt e instala as dependências
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Define diretório de trabalho e copia o restante do projeto
WORKDIR /app
COPY . /app

# Executa o app Flask
CMD ["python", "app.py"]
