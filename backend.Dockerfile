FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt

RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY database/ ./database/

# CRITICAL: Tells Python to treat /app as a root lookup directory
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["python", "-m", "backend.run"]