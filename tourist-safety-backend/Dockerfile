FROM python:3.11-slim

WORKDIR /app

# Set Python path explicitly
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run seed as module and start server  
CMD ["sh", "-c", "cd /app && python -m scripts.seed_database && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
