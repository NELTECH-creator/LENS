# LENS Backend — Cloud Run Container
# Python 3.12 slim base for minimal image size

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY *.py .

# Cloud Run uses PORT env var (default 8080)
ENV PORT=8080
EXPOSE 8080

# Run with uvicorn — Cloud Run needs 0.0.0.0 binding
CMD ["python", "main.py"]
