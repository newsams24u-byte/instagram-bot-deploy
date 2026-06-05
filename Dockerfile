# Use official Python 3.11 slim image (much smaller than full image)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install system dependencies required for Pillow and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements_deploy.txt .

# Upgrade pip, setuptools, wheel and install Python dependencies
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install -r requirements_deploy.txt

# Copy application code
COPY . .

# Create a non-root user to run the app
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port 5000 (default Flask port, Render will map this)
EXPOSE 5000

# Start the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
