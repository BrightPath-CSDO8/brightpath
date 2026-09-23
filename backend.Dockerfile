FROM python:3.12-slim

WORKDIR /app

# 1. Install Microsoft ODBC Driver 18 and build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    unixodbc-dev \
    gcc \
    g++ \
    build-essential \
    && DEBIAN_VERSION=$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1) \
    && curl -sSL -O https://packages.microsoft.com/config/debian/${DEBIAN_VERSION}/packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies (including Gunicorn and pyodbc/SQLAlchemy)
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# 3. Copy application files
COPY backend/ ./backend/
COPY database/ ./database/

ENV PYTHONPATH=/app
EXPOSE 5000

# 4. Launch with a high-performance Gunicorn configuration
CMD ["gunicorn", "--workers=2", "--threads=2", "--bind", "0.0.0.0:5000", "backend.run:app"]
