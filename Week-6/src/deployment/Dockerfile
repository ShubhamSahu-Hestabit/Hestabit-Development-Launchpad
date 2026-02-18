# =========================
# Base Image
# =========================
FROM python:3.12-slim

# =========================
# Set working directory
# =========================
WORKDIR /app

# =========================
# Install system dependencies
# =========================
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Copy requirements and install
# =========================
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# =========================
# Copy the entire src folder into container
# =========================
COPY src ./src

# =========================
# Set working directory for running API
# =========================
WORKDIR /app/src

# Expose port
EXPOSE 8000

# =========================
# Run the FastAPI app
# =========================
CMD ["uvicorn", "deployment.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
