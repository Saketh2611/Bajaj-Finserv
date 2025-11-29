# -----------------------------
# 1. Base Image
# -----------------------------
FROM python:3.11-slim

# Working directory inside container
WORKDIR /app

# -----------------------------
# 2. System Dependencies (PDF + OCR + Image Support)
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \            # required for pdf2image
    tesseract-ocr \            # OCR if used later
    libgl1 \                   # avoids cv2/openCV crashes
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 3. Environment + Python Settings
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# -----------------------------
# 4. Install Dependencies First (Better caching)
# -----------------------------
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# -----------------------------
# 5. Copy App Code
# -----------------------------
COPY . .

# -----------------------------
# 6. Expose API Port
# -----------------------------
EXPOSE 8000

# -----------------------------
# 7. Run Production Server
# -----------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
