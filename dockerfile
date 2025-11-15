# -----------------------------
# Base Python Image
# -----------------------------
FROM python:3.10-slim

# -----------------------------
# System Dependencies (for pytesseract + fitz)
# -----------------------------
RUN apt-get update && \
    apt-get install -y \
        tesseract-ocr \
        libtesseract-dev \
        build-essential \
        poppler-utils \
        libgl1-mesa-glx \
        libglib2.0-0 \
        && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Set Work Directory
# -----------------------------
WORKDIR /app

# -----------------------------
# Copy Requirements and Install
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy Django Project
# -----------------------------
COPY . .

# -----------------------------
# Collect Static Files
# -----------------------------
RUN python manage.py collectstatic --noinput

# -----------------------------
# Expose Port (Render will map it)
# -----------------------------
EXPOSE 8000

# -----------------------------
# Start Gunicorn Server
# -----------------------------
CMD ["gunicorn", "LockIn.wsgi:application", "--bind", "0.0.0.0:8000"]
