# Base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Prevent Python from writing .pyc and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (for psycopg2, pandas, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app source
COPY . /app/

# Expose port
EXPOSE 5000

# Environment variables (override in production)
ENV FLASK_ENV=production
ENV SECRET_KEY=SUPER_ENTERPRISE_KEY_2026

# Default command (gunicorn for production)
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
