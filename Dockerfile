# =========================
# Base Image
# =========================
FROM python:3.10-slim

# =========================
# Environment variables
# =========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Optional: reduce TF logs
ENV TF_CPP_MIN_LOG_LEVEL=2

# =========================
# Set working directory
# =========================
WORKDIR /app

# =========================
# System dependencies
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Copy requirements first (for cache)
# =========================
COPY requirements.txt .

# =========================
# Install Python dependencies
# =========================
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# =========================
# Copy entire project INCLUDING MODEL
# =========================
COPY . .

# =========================
# Expose Flask port
# =========================
EXPOSE 5000

# =========================
# Run Flask app
# =========================
CMD ["python", "app.py"]
