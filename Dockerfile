# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install required system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy entire application code (you can use .dockerignore to exclude unnecessary files)
COPY . .

# Set permissions (optional)
RUN chmod -R 755 /app

# Expose port (Django default)
EXPOSE 8000

# Default run command (Django server)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
