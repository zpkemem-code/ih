FROM python:3.10-slim

# Update dan instal paket yang diperlukan
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    ffmpeg git apt-utils libmediainfo0v5 sqlite3 \
    libgl1 libglib2.0-0 libxml2-dev libxslt-dev sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Buat direktori kerja dan salin file yang diperlukan
WORKDIR /app

# Salin file requirements terlebih dahulu untuk memanfaatkan cache Docker
COPY requirements.txt .

# Instal dependensi Python
RUN pip3 install -U pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Salin semua file aplikasi
COPY . .

# Buat skrip bisa dieksekusi setelah COPY
RUN chmod +x ulimit.sh start.sh

# Set variabel lingkungan
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port yang dibutuhkan
EXPOSE 7860-8000


# Set entrypoint
ENTRYPOINT ["./start.sh"]