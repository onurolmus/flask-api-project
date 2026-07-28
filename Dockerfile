FROM python:3.12-slim

WORKDIR /app

# uWSGI C ile yazılmış bir uygulama sunucusu, pip install sırasında derleniyor.
# build-essential = gcc + g++ + make + tüm standart C header dosyaları (stdio.h vs.)
# Debian slim'de bunlar yok, biz ekliyoruz.
# Kurulumdan sonra apt cache temizleniyor → image boyutu küçülüyor.
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uwsgi", "--ini", "uwsgi.ini"]
