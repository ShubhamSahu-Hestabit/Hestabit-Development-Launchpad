FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for LightGBM
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src

EXPOSE 8000

CMD ["uvicorn", "deployement.api:app", "--host", "0.0.0.0", "--port", "8000"]
