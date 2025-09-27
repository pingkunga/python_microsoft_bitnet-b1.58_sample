# Use official Python 3.12 image
FROM python:3.12-slim

# Install system dependencies for PyTorch and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        curl \
        ca-certificates \
        libopenblas-dev \
        libomp-dev \
        libssl-dev \
        libffi-dev \
        wget \
        && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# (Optional) Set a working directory
WORKDIR /app

# Copy your requirements.txt if you have one
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt


# Copy your application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Default command to run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "120"]